#!/usr/bin/env bash

set -euo pipefail

./start.sh

if [[ $# != 0 ]]; then
    "$@"
else
    tail -f /var/log/*.log
fi
