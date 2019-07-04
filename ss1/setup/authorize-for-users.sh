#!/usr/bin/env bash

set -euo pipefail

for user; do
    id "$user" >/dev/null || exit 1

    mkdir -pv "/home/$user/.ssh"
    cp -v /root/.ssh/authorized_keys "/home/$user/.ssh"
    chown -Rv "$user" "/home/$user/.ssh"
done