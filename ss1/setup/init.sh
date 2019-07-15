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
        addgroup "level$((count-1))" "$username" || :
    fi

    local rundir=$rundir/$level
    mkdir "$rundir"

    local dirname filename src dst
    for dirname in runtime code; do
        src=$content/levels/$username/$dirname
        [[ -d "$src" ]] && cp -vr "$src" "$rundir/$dirname"
    done
    for filename in start.sh; do
        src=$content/levels/$username/$filename
        [[ -f "$src" ]] && cp -v "$src" "$rundir/"
    done

    mkdir -p "$rundir/wwwdata"
    chmod 700 "$rundir/wwwdata"
    chown "$username" "$rundir/wwwdata"
}

rundir=/var/run/levels
msg "setting up '$rundir' for services ..."
mkdir -p "$rundir"
chmod 701 "$rundir"

for level in "$content"/levels/level?/; do
    level=$(basename "$level")
    create_level "$level"
done

msg "setting empty password for level0 ..."
echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config
passwd -d level0

# Note: this is needed to enable root login; the actual password doesn't matter
if grep -q '^root:!:' /etc/shadow; then
    msg "setting password for root user ..."
    password=$(cat /root/.password)
    chpasswd --md5 <<< "root:$password"
fi
