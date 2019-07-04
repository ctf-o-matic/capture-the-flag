#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

level=$(basename "$PWD")

../common/reset.sh "$level"
