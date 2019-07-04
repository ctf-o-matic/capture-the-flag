#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

. setup/common.sh

[[ $# = 1 ]] || usage "$0 level0[1-9]"

level=$1; shift

case $level in
    level0[1-9])
        num=${level#level0}
        prev=level0$((num - 1))
        ;;
    *) fatal "got $level; expected first arg to match pattern level0[1-9]" ;;
esac

crack=levels/$level/crack.sh
[[ -f "$crack" ]] || fatal "no such file: $crack"

_ssh() {
    ssh -p 8022 \
        -oStrictHostKeyChecking=no \
        -oUserKnownHostsFile=/dev/null \
        -oLogLevel=QUIET \
        "$@"
}

pw_found=$(mktemp)
pw_expected=$(mktemp)
trap 'rm "$pw_found" "$pw_expected"' EXIT

_ssh root@localhost /setup/authorize-for-users.sh "$prev"

_ssh "$prev@localhost" 's=/tmp/crack.sh; cat > $s; chmod +x $s; $s '"$level" < "$crack" | tee "$pw_found"

_ssh root@localhost cat "/home/$level/.password" | tee "$pw_expected"

if cmp "$pw_found" "$pw_expected"; then
    echo OK
else
    echo FAILED
    exit 1
fi
