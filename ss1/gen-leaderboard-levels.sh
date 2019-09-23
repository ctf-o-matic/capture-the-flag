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

for ((i = 1, j = 1; i < ${#levels[@]}; i++)); do
    level=${levels[i]}
    solution_key=$(cat "levels/$level/solution-key.txt")
    crack_script=solutions/levels/$solution_key.sh
    password=$(cat "setup/generated/levels/$level/home/.password")
    password_sha1=$(printf "$password" | sha1sum - | awk '{print $1}')
    cat << EOF
{
  "model": "leaderboard.level",
  "pk": $i,
  "fields": {
    "name": "$level",
    "solution_key": "$solution_key",
    "answer": "$password_sha1",
    "created_at": "$timestamp"
  }
}
EOF
    while read hint; do
        cat << EOF
{
  "model": "leaderboard.hint",
  "pk": $j,
  "fields": {
    "level": $i,
    "text": "$hint",
    "visible": false,
    "created_at": "$timestamp"
  }
}
EOF
        ((j++))
    done < <(sed -ne 's/"/\\\\"/g' -e 's/^# hint: //p' "$crack_script")
done | jq -s .
