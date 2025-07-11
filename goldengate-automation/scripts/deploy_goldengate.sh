#!/usr/bin/env bash
set -euo pipefail

# Update Goldengate configuration with new tables and restart processes.
# Requires SSH access to the Goldengate EC2 host.

GG_HOST=${GG_HOST:-"goldengate.example.com"}
GG_USER=${GG_USER:-"ec2-user"}
EXTRACT_FILE=${EXTRACT_FILE:-"/u01/ggate/dirprm/ext.prm"}
REPLICAT_FILE=${REPLICAT_FILE:-"/u01/ggate/dirprm/rep.prm"}
TABLE_LIST_FILE="$(dirname "$0")/../state/pending_tables.txt"

if [ ! -f "$TABLE_LIST_FILE" ]; then
  echo "No pending_tables.txt found" >&2
  exit 1
fi

scp "$TABLE_LIST_FILE" "$GG_USER@$GG_HOST:/tmp/tables.txt"

ssh "$GG_USER@$GG_HOST" bash -s <<'EOS'
set -euo pipefail
EXTRACT_FILE="$EXTRACT_FILE"
REPLICAT_FILE="$REPLICAT_FILE"
while read -r tbl; do
  echo "TABLE $tbl;" >> "$EXTRACT_FILE"
  echo "MAP $tbl, TARGET $tbl;" >> "$REPLICAT_FILE"
done < /tmp/tables.txt
/opt/ggsci/ggsci <<EOF2
STOP EXTRACT EXT1
START EXTRACT EXT1
STOP REPLICAT REP1
START REPLICAT REP1
EOF2
sleep 60
/opt/ggsci/ggsci -e "INFO EXTRACT EXT1"
/opt/ggsci/ggsci -e "INFO REPLICAT REP1"
EOS
EOF
