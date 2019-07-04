#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
name=$(basename "$PWD")

. setup/common.sh

cid=$(docker run -d -p 8022:22 --hostname "$name" "$name")

cleanup() {
    msg "cleaning up ..."
    docker stop "$cid"
}

trap 'cleanup' EXIT

for script in levels/level*/crack.sh; do
    msg "running script: $script ..."
    "$script"
done
