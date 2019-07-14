#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

. common.sh
. setup/common.sh

[[ $# = 1 ]] || usage "$0 level[1-9]"

level=$1; shift

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

_ssh root@localhost /setup/authorize-for-users.sh "$prev"

tmpdir=$(_ssh root@localhost mktemp -d)
crack=$tmpdir/crack.sh

_ssh "root@localhost" "cat > $crack" < "$local_crack"
_ssh "root@localhost" << EOF
chmod o+x "$crack"
chmod o+xw "$tmpdir"
EOF

_ssh "$prev@localhost" "$crack $level $port" | tee "$pw_found"

_ssh root@localhost << EOF
rm -vfr "$tmpdir"
grep -vxf /root/.ssh/authorized_keys "/home/$prev/.ssh/authorized_keys" > authorized_keys
chown -v "$prev" authorized_keys
mv -v authorized_keys "/home/$prev/.ssh"
EOF

_ssh root@localhost "cat /home/$level/.password" | tee "$pw_expected"

if cmp "$pw_found" "$pw_expected"; then
    echo OK
else
    echo FAILED
    exit 1
fi
