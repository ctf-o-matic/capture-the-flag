#!/usr/bin/env bash

set -euo pipefail

for user; do
    id "$user" >/dev/null || exit 1

    mkdir -vp "/home/$user/.ssh"
    cat /root/.ssh/authorized_keys >> "/home/$user/.ssh/authorized_keys"
    chown -vR "$user" "/home/$user/.ssh"
done
