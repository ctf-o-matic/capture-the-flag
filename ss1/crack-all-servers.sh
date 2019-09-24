#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. setup/common.sh

if [[ $# = 0 ]]; then
    fatal "usage: $0 path/to/servers.json"
fi

servers_json=$1

for ip_address in $(jq -r '.[].fields.ip_address' < "$servers_json"); do
    msg "$ip_address"
    ./crack-all.sh "$ip_address"
done
