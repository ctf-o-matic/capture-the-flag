#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. common.sh

reset() {
    local leveldir=$1; shift
    local level=$(basename "$leveldir")

    local home_src=$leveldir/home
    local home_dst=/home/$level

    [[ -d "$home_dst" ]]

    cp -v "$home_src"/.??* "$home_dst"
    cp -v "$home_src"/* "$home_dst"
    chown -vR "$level:$level" "$home_dst"
    chmod -v 0700 "$home_dst"

    local code_src=$leveldir/code
    local code_dst=/levels/$level

    if [[ -d "$code_src" ]]; then
        mkdir -p "$code_dst"
        cp -vR "$code_src"/* "$code_dst"
        chown -vR "$level:$level" "$code_dst"
        chmod -vR g-w,o-rwx "$code_dst"
    fi

    # TODO move this to init, or Dockerfile
    local rundir=/var/run/levels
    mkdir -p "$rundir"
    chmod 701 "$rundir"

    custom_reset=$leveldir/reset.sh
    if [[ -f "$custom_reset" ]]; then
        "$custom_reset" "$@"
    fi

    # TODO if a service, call restart now
}

for leveldir in generated/levels/level?; do
    reset "$leveldir" "$@"
done
