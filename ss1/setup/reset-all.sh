#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

for leveldir in generated/levels/level?; do
    level=$(basename "$leveldir")
    ./reset.sh "$level" "$@"
done
