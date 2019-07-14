#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

. setup/common.sh

if [[ $# = 1 ]]; then
    host=$1; shift
else
    host=localhost
fi

for script in levels/level?/crack.sh; do
    msg "running script: $script ..."
    level=$(basename "$(dirname "$script")")
    cmd ./crack.sh "$level" "$host"
done
