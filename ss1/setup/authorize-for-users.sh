#!/usr/bin/env bash

set -euo pipefail

for user; do
    id "$user" >/dev/null || exit 1

    mkdir -vp "/home/$user/.ssh"
    cp -v /root/.ssh/authorized_keys "/home/$user/.ssh"
    chown -vR "$user" "/home/$user/.ssh"
done
