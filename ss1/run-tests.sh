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

seconds=3
msg "sleep for $seconds seconds to wait for container ..."
sleep "$seconds"

./test-reset.sh

./crack-all.sh
