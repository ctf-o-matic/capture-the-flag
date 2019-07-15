#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

. setup/common.sh

if [[ $# = 1 ]]; then
    host=$1; shift
else
    host=localhost
fi

for leveldir in levels/level[1-9]/; do
    msg "running script for dir $leveldir ..."
    level=$(basename "$leveldir")
    cmd ./crack.sh "$level" "$host"
done
