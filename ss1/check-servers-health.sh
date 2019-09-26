#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. setup/common.sh

if [[ $# = 0 ]]; then
    fatal "usage: $0 path/to/servers.json"
fi

check_server() {
    local ip_address=$1
    for ((i = 1; i <= 3; i++)); do
        if ping -c1 "$ip_address" &>/dev/null; then
            return
        fi
    done
    return 1
}

servers_json=$1

for ip_address in $(jq -r '.[].fields.ip_address' < "$servers_json"); do
    printf "checking %s ..." "$ip_address"
    check_server "$ip_address" && echo ok || echo UNRESPONSIVE
done
