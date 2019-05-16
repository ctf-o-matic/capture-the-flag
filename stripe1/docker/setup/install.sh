#!/usr/bin/env bash
#

msg() {
    echo "[*] $*"
}

cmd() {
    echo "[cmd] $*"
    $*
}

error() {
    echo "[E] $*"
    exit 1
}

set -euo pipefail

cd /setup
chmod 700 .

levelCounter=0

add_level() {
    local homeDir=$1
    local username=${homeDir##*/}
    local level=$((levelCounter++))

    local password=$(cat "$homeDir/.password")
    local uid=110$levelCounter
    adduser -s /bin/bash -u "$uid" -D "$username"
    echo "$username:$password" | chpasswd --md5

    if [ $level != 0 ]; then
        addgroup "level0$((level-1))" "$username"
    fi

    if [ -f "/levels/$username/Makefile" ]; then
        (cd "/levels/$username" && make)
    fi

    chmod -R go-rwxs "/home/$username"
    chown -R $uid:$uid "/home/$username"
    [ $level != 0 ] || return 0

    chmod 0750 "/levels/$username"
    chown -R $uid:$uid "/levels/$username"
    to_setuid=/levels/$username/$username
    test -f "$to_setuid" && chmod 4755 "$to_setuid" || :
}

for homeDir in /home/level*; do
    add_level "$homeDir"
done
