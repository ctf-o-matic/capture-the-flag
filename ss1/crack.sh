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

crack=/tmp/crack.sh

_ssh root@localhost /setup/authorize-for-users.sh "$prev"
_ssh root@localhost rm -f "$crack"

_ssh "$prev@localhost" "cat > $crack; chmod +x $crack; $crack $level $port" < "$local_crack" | tee "$pw_found"

_ssh root@localhost cat "/home/$level/.password" | tee "$pw_expected"

if cmp "$pw_found" "$pw_expected"; then
    echo OK
else
    echo FAILED
    exit 1
fi
