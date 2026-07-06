# CerbUI.Calendar — inline day/week/month/year calendar

A zero-dependency, inline calendar (NOT a popup like `CerbUI.DatePicker`) with day/week/month/year views,
multiple event **sources** shown at once (like chart series + a legend), true multi-day **spanning strips**,
year-view pips + tooltips with drill-down, and a click-to-create hook. Modeled on `CerbUI.DatePicker`; shares
month-grid math + timezone logic via a pure-logic sibling.

Files: `resources/js/cerb-ui/calendar-core.js` (pure, headless-testable, no DOM) + `calendar.js` (component) +
`layout/cerb-ui/_calendar.scss` (skin only — see "geometry in JS" below). Registration = the standard **5
spots** (`calendar-core` BEFORE `calendar`, after `datepicker`): dev loader `templates/cerb_ui_scripts.tpl`,
`composer.json` build-js terser list, `@import` in `layout/cerb-ui.scss`, gallery partial + `index.tpl` nav.
Live example = UI Reference → **Calendar** (`ui_reference/components/calendar.tpl`), not this doc.

## Public API

`new CerbUI.Calendar(el, opts)` — renders inline into `el`. Key `opts`: `views` (`['day','week','month','year']`),
`defaultView`, `date`, `startOfWeek` (`'mon'|'sun'`), `dayStartHour`/`dayEndHour`/`hourHeight`, `timeFormat`
(`'12h'|'24h'`), **`tz`** (IANA name, DST-aware — see below), `sources[]`, `showLegend`, `maxPerDay`,
`calendarId` (for the default create peek), and hooks `onEventClick`/`onCellClick`/`onCreate`/`onDrillDown`/
`onRangeChange` (each returning `false` suppresses the default).

- **Source descriptor:** `{id, label, color, icon?, visible?, events?[] | fetch?(startSec,endSec), serverShape?}`.
  Exactly one of `events`/`fetch`. `fetch` gets **epoch-SECONDS** range bounds and resolves to a flat array OR
  the raw day-keyed `Model_Calendar::getEvents()` map when `serverShape:true` (auto de-duped).
- **Raw event in:** `{label, icon?, color?, start, end, allDay?, url?, context?, contextId?}` (epoch seconds).
- **Methods:** `setView/getView`, `setDate/getDate`, `next/prev/today`, `addSource/removeSource/toggleSource`,
  `refresh` (the ONLY refetch path — clears cache), `getEvents`, `destroy`. Static `from(el)`.
- **DOM events** on `el` (bubbles): `cerb-ui-calendar:{viewchange,datechange,rangechange,eventclick,cellclick,create,sourcetoggle}`.

Internal: state = `{view, viewDate, sources:Map, _range, _cache, _fetchSeq}`. Fetch is parallel
`Promise.allSettled` across ALL sources (even hidden → toggling is instant from cache), guarded by a
`_fetchSeq` token (DatePicker's stale-drop). Chrome (nav + `CerbUI.Switcher` + legend) built once; only
`.cerb-ui-calendar--body` re-renders. **`CerbUI.Legend` is passive** (no toggle) → the calendar builds its own
`--legend-item`s + `is-off` class + click handler. Month range = the **full 42-cell grid** (so strips bleeding
from adjacent months are fetched), not the calendar month.

## calendar-core.js (`CerbUI.cal`) — pure helpers

`monthGridCells(y,m0,mode)` (42 cells, prev/next padding), `startOfWeekDate`/`weekDays`, `dayBounds`/`dayStartSec`/
`dayMidnightSec`/`minutesOfDay`/`epochParts` (tz-aware, below), `inferAllDay`/`spanDays`,
**`dedupeServerEvents(dayKeyedMap)`** (server splits a multi-day event into one clamped copy PER DAY but every
copy carries un-clamped `ts_range_start`/`ts_range_end`; dedupe key = **`context_id + ':' + ts_range_start`** —
must include start or recurring occurrences that share `context_id` collapse into one), **`packColumns(items)`**
(greedy day/week overlap columns), **`assignLanes(events)`** (global lane per strip so a multi-week event keeps
the same track wrapping week→week).

## Timezone — IANA name, DST-aware (the hard lesson)

Server event epochs are **absolute UTC seconds** but day-bucketed in some timezone (the calendar's `timezone`,
or the server/worker default for "viewer's timezone"). The client must interpret them in **that same zone**.

**DO pass an IANA name** (`tz: 'America/Los_Angeles'`), resolved via `Intl.DateTimeFormat` per-date so DST is
correct. `null`/`''` = the browser's local zone (also DST-aware via native `Date`). A **fixed offset number**
(minutes east of UTC) is legacy and **NOT DST-aware** — it's an hour off in the other season.

> **The bug this fixed:** passing a fixed offset computed at "now" (summer PDT, −7) made winter all-day events
> (Christmas/New Year/Thanksgiving, PST −8) read an hour late → their `23:59:59` end rolled into the next day →
> a bogus 2-day span; summer events (Jul 4/Labor Day) were fine. **Never interpret year-round server epochs
> with a single fixed offset.**

`dayStartSec(y,m,d, ianaZone)` = UTC-guess for midnight, correct by the zone's offset at the guess, then
re-check once (handles the offset changing across a DST edge). all-day inference tolerates `>= 86340` (not exact
`86399`) for DST-short days. Node ships full ICU, so all of this is **headless-testable** (assert every US
holiday spans exactly 1 day in `America/Los_Angeles`).

## Rendering model — geometry in JS, skin in CSS

Positions/heights/lane offsets are computed in JS and applied inline; `_calendar.scss` is colors/tokens only
(like the chart family). Month = 6 week-rows, each a `--daycells` grid + an absolutely-positioned `--strips`
overlay (`pointer-events:none` except the bars, so empty-cell clicks pass through to create). Strip radius:
left-rounded only in the row containing the true start, right-rounded only at the true end, else
`--continues-left/right` (flat). Day/week = a scrollable 24h vertical grid; timed events absolutely positioned
(`top` from `minutesOfDay`, height from duration), overlaps column-packed; all-day/multi-day → a pill band up
top. Year = 12 mini-months (reuse `monthGridCells`), one `.cerb-ui-pip` per contributing source, one shared
`CerbUI.Tooltip` for day details. Year highlights **today only in its own month** (gate on `cell.inMonth`).

## Widget integration (profile / workspace / card)

All three calendar widgets render client-side now — **no per-nav server round-trip** (the old `showCalendarTab`
action is gone). Shared host: **`Model_Calendar::displayCerbUiWidget($tpl, $worker, $default_view='month')`**
assigns a JSON config (dom id, calendar id, `tz` name, week start, legend color = the calendar's
`color_available`) + displays **`internal/calendar/widget_cerb_ui.tpl`**, which boots a `CerbUI.Calendar` with
one source (`serverShape:true`) whose `fetch` hits the JSON endpoint. Each widget's `render()` resolves the
calendar (placeholder-expanded `calendar_id`) + reads a per-instance **`default_view`** from its config
(`extension_params` for profile/card, `params` for workspace; validated against the whitelist in the host).
Card widget = a new `Extension_CardWidget` (`cerb.card.widget` plugin.xml block, icon `calendar`) — **needs
`/update`** to register. Availability widget left alone (different synthesized-events data model).

## Reusable `c=ui` JSON endpoint pattern

Client: `genericAjaxGet('', 'c=ui&a=<action>&k=v', cb)` (empty URL + query string; `cb` gets parsed JSON).
`Engine::readRequest` turns `c=ui&a=foo` into `$request->path = ['ui','foo']` (the `a=` value is filtered to
`[A-Za-z0-9_]`). Add a `case '<action>': return $this->_uiAction_<action>();` to `Controller_UI::_invoke`
(the switch is alphabetical) + the method — set `Content-Type: application/json`, ACL-check, `echo json_encode`.
`Controller_UI` already requires an active worker. Example: `calendarEventsJson` returns a calendar's
`getEvents($from,$to)` as day-keyed `{events:{ts:[…]}}`, **without occlusion** (occlusion only trims/splits
`is_available` blocks and would fragment spanning strips). `DevblocksDictionaryDelegate` IS `JsonSerializable`
(→ its underlying dict) if you ever return dicts directly.

## Reusable primitives spun out

- **`CerbUI.color`** (in `palettes.js`, general — not calendar-specific): `parseHex`, `luminance` (WCAG 0–1),
  `contrastRatio` (1–21), **`idealTextColor(bg)`** → near-black `#141414` or `#ffffff` for the higher contrast
  (null for a non-hex value → defer to CSS). Use it for legible labels on ANY arbitrary fill (tag/event/chart/
  user color) since we now have light+dark themes — white-on-light-pastel is illegible. Demoed in the UI Ref
  **Utilities** gallery ("Color · contrast").

## Gotchas

- **Global `BUTTON { height: 2.4em }` clips/bloats content `<button>`s.** Any multi-line or compact button (a
  day-column header with dow+number, list rows, "+N more", captions) needs **`height: auto`** or the fixed
  height clips it (a header number overflowed onto the grid line). Same family as the global `BUTTON:hover`
  gotcha in `scss-build.md`. Buttons whose height you set inline (JS) are exempt.
- **Scrollable hour grid needs top padding** so the first hour line + "12 AM" label clear the day-number header.
- Wrap the widget-host JS in `{literal}`; inject the PHP JSON config with a single `{/literal}{$json nofilter}{literal}`
  hop (json_encode with `JSON_HEX_TAG|JSON_HEX_AMP|JSON_HEX_APOS|JSON_HEX_QUOT` so a calendar name can't break out).
- Headless test harness: stub `CerbUI`, a tiny DOM (createElement/classList/style/dataset/appendChild/…), load
  `palettes.js`+`calendar-core.js`+`switcher.js`+`calendar.js`, assert each view renders + the pure helpers
  (dedup, lanes, packing, tz/DST, contrast). Full ICU in Node makes the tz tests real.
