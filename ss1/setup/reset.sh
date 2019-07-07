#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. common.sh

for script in generated/levels/level?/reset.sh; do
    cmd "$script" "$@"
done
