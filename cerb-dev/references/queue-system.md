# Queue System Reference

Cerb's parallel background queue runs producer → consumer work via three tables: `queue` (named queues), `queue_message` (units of work), `queue_job` (bounded multi-message operations with progress).

## Anatomy

| Table | Purpose | Lifecycle |
|---|---|---|
| `queue` | Named queue + which `Extension_QueueConsumer` handles it | Permanent |
| `queue_message` | One unit of work (UUID PK, JSON payload, status) | Purged 24h after status=DONE (`DAO_QueueMessage::maint`) |
| `queue_job` | Optional bounded operation that owns N messages, with progress counters | Kept indefinitely (audit trail); admin-only delete |
| `queue_job_chunk` | Per-job staging blob storage when a job needs parallel-produce → ordered-reassemble | Deleted at job completion |

`queue_message.job_id = 0` means "no parent job" — fire-and-forget. Otherwise messages roll progress up to their parent job.

`QueueJobStatus` enum: `RUNNING=0`, `PAUSED=1`, `DONE=2`. Only three states despite older planning docs mentioning more.

**`count_total` on `queue_job` = number of queue MESSAGES (batches), not records.** If a job batches 100 records per message and exports 10,000 records, `count_total=100`. Store the actual record count in `metadata.record_count` if you need it for audit.

## Writing a Consumer Extension

Extend `Extension_QueueConsumer`:

```php
class QueueConsumer_MyKind extends Extension_QueueConsumer {
    const ID = 'cerb.queue.consumer.mykind';

    function renderConfig(Model_Queue $model): void {}
    function invokeConfig($action, Model_Queue $model): void {}

    public function processQueueMessages(
        Model_Queue $queue, int $stop_time, int $count_hint, ?Model_QueueJob $queue_job=null
    ): int {
        if($queue->name == 'my.queue.name') {
            // dequeue a batch, do work, reportSuccess/reportFailure
        }
        return 0;
    }

    // Optional. Fires exactly once when the queue_job transitions to DONE.
    // Stateless context — runs in the cron's shutdown, no active worker/visit.
    public function onQueueJobComplete(\Model_QueueJob $queue_job): void {
        // Finalize: assemble chunks, send notifications, etc.
    }
}
```

Register in `plugin.xml` under extension point `cerb.queue.consumer`. Register the queue itself in a patch:

```php
if(!$db->GetOneMaster("SELECT id FROM queue WHERE name = 'my.queue.name'"))
    $db->ExecuteWriter("INSERT IGNORE INTO queue (name, created_at, updated_at, extension_id) VALUES ('my.queue.name', UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), 'cerb.queue.consumer.mykind')");
```

## Where `publish()` Runs

`_DevblocksQueueService::publish()` flushes status updates and fires `onQueueJobComplete`. It runs in `Devblocks::shutdown()`, registered as a PHP shutdown function.

| Context | Has `getActiveWorker()` / `getVisit()`? |
|---|---|
| FPM request | Yes |
| `cron/background_queue` | **No** — stateless |

The export consumer is drained by the cron, so its `onQueueJobComplete` runs stateless. Anything that needs a session (e.g. `C4_AbstractView::marqueeAppend`) won't work here — surface results via persistent mechanisms (notifications, attachment links, metadata flags).

## Exactly-Once Completion Hook (GET_LOCK)

Two parallel consumers can both observe a job's last batch finishing, both call `checkForCompletedJobs`, and both try to fire `onQueueJobComplete`. Guard with a per-job MySQL advisory lock:

```php
foreach($newly_finished_jobs as $job) {
    $lock = sprintf('cerb_queue_job_complete:%d', $job->id);
    if(!$db->GetOneMaster(sprintf("SELECT GET_LOCK(%s, 0)", $db->qstr($lock))))
        continue;  // someone else owns finalization
    try {
        // Re-check status with master — another process may have just finished
        $current = DAO_QueueJob::get($job->id);
        if(!$current || $current->status_id == QueueJobStatus::DONE->value)
            continue;
        DAO_QueueJob::setStatus([$job->id], QueueJobStatus::DONE);
        if(($queue = DAO_Queue::get($current->queue_id)) && ($ext = $queue->getExtension()))
            $ext->onQueueJobComplete($current);
    } catch(Throwable $e) {
        DevblocksPlatform::logException($e);
    } finally {
        $db->ExecuteWriter(sprintf("DO RELEASE_LOCK(%s)", $db->qstr($lock)));
    }
}
```

Properties: `GET_LOCK(name, 0)` is non-blocking. Lock is instance-local (no replica replication) and **auto-released on connection close** — a crashed FPM worker doesn't strand it.

The slot-acquisition pattern in `_DevblocksQueueService::getConcurrencySlot()` is the same primitive at a different granularity (N numbered slots for concurrency limiting).

## Abstract Job-Complete Notification

Every `queue_job` that finalizes with `worker_id != 0` automatically generates a `DAO_Notification` for that worker, fired from `_DevblocksQueueService::_finalizeJobs` between `setStatus(DONE)` and `onQueueJobComplete`. The notification's `entry_json.urls.target = cerb:cerberusweb.contexts.queue.job:<id>` — clicking opens the queue_job peek (which surfaces consumer-specific results via the Monitor widget — attachments for export, status only for bulk update, etc.).

**Consumers should NOT fire their own completion notifications.** The abstract layer covers it. The activity point is `cerb.queue.job.completed`, registered in `plugin.xml`. Workers can suppress per activity-point via the `dont_notify_on_activities` worker pref.

If a consumer needs more than the abstract notification (e.g. a custom CTA, a richer message), it can additionally fire its own notification with a custom activity point — both will fire. The abstract one is always-on for any worker-owned job.

`worker_id == 0` jobs (system maintenance, fire-and-forget) get no notification, which is the right default.

## Producer: Bulk Enqueue in One SQL

For `queue_job`-based jobs that batch IDs from a known set (worklist filter, full table scan, etc.), generate every queue message in a single `INSERT...SELECT` rather than looping `enqueue()` in PHP:

```php
$inner_select_sql =
    "SELECT " . $primary_key . " AS id " .
    $query_parts['join'] .
    $query_parts['where'] .
    " GROUP BY " . $primary_key   // dedupe in case joins multiplied rows
;

$sql = sprintf(
    "INSERT INTO queue_message (uuid, queue_id, job_id, status_id, status_at, message) ".
    "SELECT UUID_TO_BIN(UUID()) AS uuid, ".
    "%d AS queue_id, ".
    "%d AS job_id, ".
    "0 AS status_id, ".
    "UNIX_TIMESTAMP() AS status_at, ".
    "CONCAT('{\"chunk\":', batch, ',\"ids\":[', GROUP_CONCAT(id ORDER BY id), ']}') AS message ".
    "FROM (SELECT id, CEIL(ROW_NUMBER() OVER (ORDER BY id) / %d) AS batch FROM (%s) AS deduped) AS batched ".
    "GROUP BY batch",
    $queue->id, $queue_job->id, $batch_size, $inner_select_sql
);
$db->ExecuteMaster($sql);
```

`ROW_NUMBER() OVER (ORDER BY ...) / batch_size` assigns each record to a chunk; `GROUP_CONCAT(id ORDER BY id)` packs each chunk's IDs into one message payload; the outer `GROUP BY batch` produces one `INSERT` row per chunk.

The `chunk` index in the payload is the ordering key — preserve it through the consumer if reassembly order matters.

Reference implementations: `SearchIndex_Fulltext::_reindexCreateJob` (no filter), `_internalAction_saveExport` in `worklists.php` (with worklist filter — uses `getSearchQueryComponents` + `GROUP BY` to dedupe joins).

## Batching Strategy: Per-Record vs Batched Payload

When designing a new queue producer, decide whether each `queue_message` carries one record ID or a batch of N. The two patterns in tree:

| Pattern | Used by | Why |
|---|---|---|
| **One ID per message** | `cerb.records.import` | Each record is a discrete file-seek + parse — work is independent and lookup-bound. Per-message granularity is cheap because the producer is already reading the file linearly. |
| **N IDs per message** (batched) | `cerb.records.export`, `cerb.records.bulk_update`, `cerb.search.index` | Work is uniform DB ops where batching dramatically reduces overhead. Per-record overhead would be punishing at scale (10M-record reindex). |

**Default to batched (N=100)** unless each record genuinely needs its own discrete unit of work. Reasons:

- Storage: a batched 100K-record job uses ~750 KB of `queue_message` rows vs ~6.3 MB if per-record (plus 100× fewer UUIDs generated, 100× fewer rows for maint to purge).
- Atomicity: most `DAO_X::bulkUpdate()` and `DAO_X::reindex()` style operations are already all-or-nothing per batch — batched payloads inherit that naturally.
- Backpressure: the cron's 25s budget is the natural limit. If a batch takes 18s, the cron just doesn't get to the next one this tick. Browser monitors are decoupled.

**Don't add a `cardinality` column to `queue_message` on a whim.** The progress display showing "11/11" instead of "1014/1014" for a batched job is a known cost. Adding cardinality is the right answer if/when work-unit routing heuristics need it (lighter messages preferred), but for display alone the producer can stash `record_count` in `queue_job.metadata` for audit.

## Parallel Produce → Ordered Reassemble (`queue_job_chunk`)

When parallel consumers each produce output bytes that must later be assembled in order (exports, batched LLM output, report generation), use the generic `queue_job_chunk` table — one row per chunk, blob payload, ordered by `chunk_idx`. Don't build per-job tables.

Producer (in consumer's `processQueueMessages`):
```php
\DAO_QueueJobChunk::put($queue_job->id, $chunk_idx, $bytes);
```

Reassembler (in `onQueueJobComplete`):
```php
\DAO_QueueJobChunk::streamByJobId($queue_job->id, function($data, $chunk_idx) use ($fp) {
    fwrite($fp, $data);
});
\DAO_QueueJobChunk::deleteByJobIds([$queue_job->id]);  // chunks are ephemeral
```

Chunks deleted at completion. InnoDB reuses freed pages — no `OPTIMIZE TABLE` needed under steady-state churn. Same pattern protects `queue_message` via its 24h purge.

## Cron Architecture

`Cron_BackgroundQueue` (every minute, 25s budget) polls `queue_message` for available work, groups by queue, shuffles for fairness, and dispatches via `$queue_extension->processQueueMessages()`. Excludes the `cerb.queue.consumer.manual` queue (UI-only).

## Claims, Retries, and Reaping

`dequeue()` claims messages by setting `status_id=IN_FLIGHT`, a random `claim_id` (binary(16), returned by-ref to the consumer), and `claimed_at`. A failure reported before the queue's `retry_max` is exhausted returns the message to `AVAILABLE` with `claim_id=NULL`, `retry_count+1`, and an exponential backoff via `available_at` (`_DevblocksQueueService::getRetryBackoffSecs()` spreads `retry_max` attempts across the queue's `retry_window_secs`); after that it goes terminal `FAILED`.

Stalled claims are reaped: a message `IN_FLIGHT` longer than its queue's `claim_window_secs` (default 3600; 0 = never reap) is treated exactly like a reported failure. `Cron_BackgroundQueue::run()` calls `_DevblocksQueueService::reapStalledMessages()` every minute (covers manual queues too): it feeds `DAO_QueueMessage::getStalled()` models through the normal `reportFailure()` path — metrics, per-job log entry, retry backoff or terminal FAILED, job sync + finalization — and flushes immediately via `publish()`. The claim window is the consumer's completion deadline; size it generously above the slowest expected batch.

## Existing Internal Queues

| Queue | Purpose |
|---|---|
| `cerb.metrics.publish` | Metrics aggregation flush |
| `cerb.records.changed` | `record.changed` automation event dispatch |
| `cerb.records.import` | Worklist imports (CSV/JSONL → records) |
| `cerb.records.export` | Worklist exports (records → CSV/JSON/JSONL/XML) |
| `cerb.records.bulk_update` | Worklist bulk update (apply field changes to N records) |
| `cerb.search.index` | Full-text reindex |

All handled by the single `QueueConsumer_Internal` extension which dispatches by queue name.
