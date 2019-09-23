#!/usr/bin/env bash
#
# Generate JSON data for leaderboard servers
#

set -euo pipefail

if ! [[ -f main.tf ]]; then
    echo "No main.tf file. Run this script from inside a terraform workspace."
    exit 1
fi

timestamp=$(date "+%Y-%m-%dT%H:%M:%SZ")

i=0
while read ip_address; do
    ((i++)) || :
    cat << EOF
{
  "model": "leaderboard.server",
  "pk": $i,
  "fields": {
    "ip_address": "$ip_address",
    "created_at": "$timestamp"
  }
}
EOF
done < <(terraform show | sed -ne '/nat_ip/s/.*= //p' | tr -d '"') | jq -s .
