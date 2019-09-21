#!/usr/bin/env bash
#
# Dump on stdout the list of authorized keys
#

set -euo pipefail

cd "$(dirname "$0")"
. setup/common.sh

loadConfig

if [[ ${#authorized_github_users[@]} != 0 ]]; then
    for username in "${authorized_github_users[@]}"; do
        curl -s "https://github.com/$username.keys" | sed -e "s/\$/ $username@github/"
    done
else
    ssh-add -L || error "no keys in ssh-agent; you might want to add some and re-run"
fi
