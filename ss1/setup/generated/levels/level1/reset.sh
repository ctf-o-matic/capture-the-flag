#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

level=$(basename "$PWD")

../common/reset.sh "$level"

cd special
make

progpath=/levels/$level/prog
cp prog "$progpath"
chown -v "$level:$level" "$progpath"
chmod -v 4555 "$progpath"
