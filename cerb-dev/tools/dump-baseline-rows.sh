#!/usr/bin/env bash
# Dump seed rows from a fresh Docker install and rewrite hard-coded
# Unix timestamps to UNIX_TIMESTAMP() so install-time stamping works.
# Output is suitable for install/sql/cerb_base_rows.sql.
#
# Usage: dump-baseline-rows.sh [--user USER] [--pass PASS] [--db DB] <mysql_container_id> > cerb_base_rows.sql
#
# Defaults match install/docker/.env.template:
#   --user cerb  --pass s3cr3t  --db cerb

set -euo pipefail

db_user="cerb"
db_pass="s3cr3t"
db_name="cerb"
container_id=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --user) db_user="$2"; shift 2 ;;
        --pass) db_pass="$2"; shift 2 ;;
        --db)   db_name="$2"; shift 2 ;;
        -h|--help)
            sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//' >&2
            exit 0
            ;;
        --) shift; container_id="${1:-}"; break ;;
        -*) echo "Unknown option: $1" >&2; exit 1 ;;
        *)  container_id="$1"; shift ;;
    esac
done

if [[ -z "$container_id" ]]; then
    echo "Usage: $0 [--user USER] [--pass PASS] [--db DB] <mysql_container_id> > cerb_base_rows.sql" >&2
    exit 1
fi

# --ignore-table list: tables the installer/seed already populates
# (cerb_class_loader, cerb_extension, cerb_event_point, translation),
# transient runtime state (devblocks_session, context_avatar, resource,
# storage_resources, package_library), or content regenerated from KATA
# (automation). The arg form is `--ignore-table=<db>.<table>`, so the
# database name has to be interpolated here.
#
# Timestamp rewrite — two ordered passes. The prefix alternation
# `1[7-9]\d{8}|2\d{9}` covers ~Nov 2023 through ~Jan 2065 so it survives
# the decade rollover that an `17\d{8}`-style rule wouldn't.
#
#   Pass 1: quoted form  '1730000000' -> UNIX_TIMESTAMP() (drops the quotes
#           too — required for cerb_property_store where `value` is text;
#           leaving '...' would store the literal string 'UNIX_TIMESTAMP()'
#           instead of a resolved function call).
#   Pass 2: bare form    1730000000   -> UNIX_TIMESTAMP()
#
# Pass 1 MUST run first; otherwise pass 2 strips the digits and leaves
# stranded single quotes.
#
# Double-quoted perl source so we can use literal `'` inside the regex
# without the `'\''` shell escape dance.
docker exec "$container_id" mysqldump \
    --compact --default-character-set=utf8mb3 --no-tablespaces \
    --skip-column-statistics --skip-opt -t \
    "--ignore-table=${db_name}.automation" \
    "--ignore-table=${db_name}.cerb_class_loader" \
    "--ignore-table=${db_name}.cerb_event_point" \
    "--ignore-table=${db_name}.cerb_extension" \
    "--ignore-table=${db_name}.context_avatar" \
    "--ignore-table=${db_name}.resource" \
    "--ignore-table=${db_name}.storage_resources" \
    "--ignore-table=${db_name}.package_library" \
    "--ignore-table=${db_name}.devblocks_session" \
    "--ignore-table=${db_name}.translation" \
    -u "$db_user" "-p${db_pass}" "$db_name" \
  | grep -v '^/\*\!' \
  | perl -pe "
      s/'(?:1[7-9]\d{8}|2\d{9})'/UNIX_TIMESTAMP()/g;
      s/\b(?:1[7-9]\d{8}|2\d{9})\b/UNIX_TIMESTAMP()/g;
    "
