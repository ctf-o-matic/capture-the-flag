#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
chmod 700 .

./init.sh
./reset.sh
