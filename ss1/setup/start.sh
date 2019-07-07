#!/usr/bin/env bash

set -euo pipefail

. /setup/common.sh

./start-ssh-server.sh
waitForPort 22

services=(/var/run/levels/level?)
if [[ -d "${services[0]}" ]]; then
    for service in "${services[@]}"; do
        level=$(basename "$service")
        /setup/service.sh "$level" start
    done
fi

netstat -ntlp
