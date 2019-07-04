#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. common.sh

content=generated

is_numeric() {
    case $1 in
        ''|*[!0-9]*) return 1 ;;
        *) return 0 ;;
    esac
}

create_level() {
    local username=$1
    if id "$username" &>/dev/null; then
        msg "user exists, skipping: $username"
        return
    else
        msg "create user: $username"
    fi

    local count=${username: -1}
    is_numeric "$count" || fatal "not numeric count: $count"
    local uid=110$count

    local password=$(cat "$content/levels/$username/home/.password")
    [[ "$password" ]] || fatal "empty password (maybe .password file missing?)"

    adduser -s /bin/bash -u "$uid" -D "$username"
    echo "$username:$password" | chpasswd --md5

    if [ $count != 0 ]; then
        addgroup "level0$((count-1))" "$username"
    fi
}

for level in "$content"/levels/level*/; do
    level=$(basename "$level")
    create_level "$level"
done

if grep -q '^root:!:' /etc/shadow; then
    msg "setting password for root user ..."
    password=$(cat /root/.password)
    chpasswd --md5 <<< "root:$password"
fi

echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config
passwd -d level00
