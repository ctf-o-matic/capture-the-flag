#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

. common.sh
. setup/common.sh

[[ $# == [12] ]] || usage "$0 level[1-9] [host]"

level=$1; shift

if [[ $# = 1 ]]; then
    host=$1; shift
else
    host=localhost
fi

case $level in
    level[1-9])
        num=$(num "$level")
        prev=level$((num - 1))
        ;;
    *) fatal "got $level; expected first arg to match pattern level[1-9]" ;;
esac

port=$(levelport "$level")

local_crack=levels/$level/crack.sh
[[ -f "$local_crack" ]] || fatal "no such file: $local_crack"

pw_found=$(mktemp)
pw_expected=$(mktemp)
trap 'rm "$pw_found" "$pw_expected"' EXIT

as_root() {
    _ssh "root@$host" "$@"
}

as_user() {
    _ssh "$prev@$host" "$@"
}

as_root /setup/authorize-for-users.sh "$prev"

tmpdir=$(as_root mktemp -d)
crack=$tmpdir/crack.sh

as_root "cat > $crack" < "$local_crack"
as_root << EOF
chmod o+x "$crack"
chmod o+xw "$tmpdir"
EOF

as_user "$crack $level $port" | tee "$pw_found"

as_root << EOF
rm -vfr "$tmpdir"
grep -vxf /root/.ssh/authorized_keys "/home/$prev/.ssh/authorized_keys" > authorized_keys
chown -v "$prev" authorized_keys
mv -v authorized_keys "/home/$prev/.ssh"
EOF

as_root "cat /home/$level/.password" | tee "$pw_expected"

if cmp "$pw_found" "$pw_expected"; then
    echo OK
else
    echo FAILED
    exit 1
fi
