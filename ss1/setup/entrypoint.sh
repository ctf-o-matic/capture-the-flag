#!/usr/bin/env bash

set -euo pipefail

./start.sh

if [[ $# != 0 ]]; then
    "$@"
else
    logs=(/var/log/*.log)
    if [[ -f "${logs[0]}" ]]; then
        tail -f /var/log/*.log
    else
        while :; do
            date
            sleep 5
        done
    fi
fi
