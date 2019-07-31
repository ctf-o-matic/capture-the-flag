#!/usr/bin/env bash
#
# Generate JSON data for leaderboard levels
#

set -euo pipefail

cd "$(dirname "$0")"
. setup/common.sh

# directories matching "level?"
levels=(levels/level?/)
# strip trailing "/"
levels=(${levels[@]%/})
# strip beginning, leaving only the directory name
levels=(${levels[@]##*/})

timestamp=$(date "+%Y-%m-%dT%H:%M:%SZ")

for ((i = 1; i < ${#levels[@]}; i++)); do
    level=${levels[i]}
    password=$(cat "setup/generated/levels/$level/home/.password")
    password_sha1=$(printf "$password" | sha1sum - | awk '{print $1}')
    cat << EOF
{
  "model": "leaderboard.level",
  "pk": $i,
  "fields": {
    "name": "$level",
    "answer": "$password_sha1",
    "created_at": "$timestamp"
  }
}
EOF
done | jq -s .
