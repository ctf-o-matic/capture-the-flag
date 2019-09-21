#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. common.sh

reset() {
    local level=$1; shift

    local leveldir=generated/levels/$level

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
        chmod -v 0750 "$code_dst"
        chmod -vR g-w,o-rwx "$code_dst"
    fi

    chmod 0700 "/var/run/levels/$level/wwwdata"

    custom_reset=$leveldir/reset.sh
    if [[ -f "$custom_reset" ]]; then
        "$custom_reset" "$@"
    fi

    if [[ $# == 0 ]]; then
        /setup/service.sh "$level" restart || :
    fi
}

[[ $# != 0 ]] || fatal "usage: $0 LEVELNAME"

reset "$@"
