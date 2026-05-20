#!/usr/bin/env bash
# Dump the schema DDL from a fresh Docker install and normalize it into
# the baseline format used by install/sql/cerb_base_tables.sql.
#
# Usage: dump-baseline-tables.sh [--user USER] [--pass PASS] [--db DB] <mysql_container_id> > cerb_base_tables.sql
#
# Defaults match install/docker/.env.template:
#   --user cerb  --pass s3cr3t  --db cerb
#
# Run against a Docker MySQL container after the guided installer has
# applied all patches but BEFORE the admin account is configured.

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
            sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//' >&2
            exit 0
            ;;
        --) shift; container_id="${1:-}"; break ;;
        -*) echo "Unknown option: $1" >&2; exit 1 ;;
        *)  container_id="$1"; shift ;;
    esac
done

if [[ -z "$container_id" ]]; then
    echo "Usage: $0 [--user USER] [--pass PASS] [--db DB] <mysql_container_id> > cerb_base_tables.sql" >&2
    exit 1
fi

# mysqldump flags:
#   -d                          schema only, no rows
#   --skip-opt                  suppresses DROP TABLE, LOCK TABLES, etc.
#   --compact                   no headers/comments
#   grep -v '^/*!'              defense in depth for any /*!40101...*/ conditional comments
#
# perl pipeline (order matters):
#   1. strip table-level ` AUTO_INCREMENT=N` counters (column-level
#      `NOT NULL AUTO_INCREMENT` has no `=`, so it survives).
#   2. strip ` CHARACTER SET utf8mb3` — redundant when the table default
#      is already utf8mb3. ` CHARACTER SET utf8mb4` is preserved for
#      columns that intentionally differ (automation.script, comment.comment).
#   3. delete newlines outright — produces the `…)) ENGINE=InnoDB` collapse
#      where the last KEY meets the closing paren.
#   4. split into one statement per line.
#   5. collapse the 2-space mysqldump indent (now adjacent to commas) to single spaces.
docker exec "$container_id" mysqldump \
    --compact --default-character-set=utf8mb3 --no-tablespaces \
    --skip-column-statistics --skip-opt -d \
    -u "$db_user" "-p${db_pass}" "$db_name" \
  | grep -v '^/\*\!' \
  | perl -0777 -pe '
      s/ AUTO_INCREMENT=\d+//g;
      s/ CHARACTER SET utf8mb3//g;
      s/\n//g;
      s/;/;\n/g;
      s/ {2,}/ /g;
    '
