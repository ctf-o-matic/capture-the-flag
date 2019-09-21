#!/usr/bin/env bash

usage() {
    echo "Usage: $*"
    exit 1
}

msg() {
    echo "* $*"
}

cmd() {
    echo "[cmd] $*"
    "$@"
}

error() {
    echo "[error] $*" >&2
}

fatal() {
    echo "[fatal] $*" >&2
    exit 1
}

num() {
    local value=$1
    value=${value//[^0-9]/}
    if [[ "$value" ]]; then
        echo $((value + 0))
    fi
}

levelport() {
    local level=$1
    local num=$(num "$level")
    local port
    ((port = 8000 + num))
    echo "$port"
}

is_valid_level() {
    local level=$1
    [[ $level == level[0-9] ]]
}

findPidByPort() {
    [[ $# == 1 ]] || usage "findPidByPort port"
    local port=$1; shift

    local line=($(netstat -ntlp | grep ":$port "))
    [[ ${#line[@]} != 0 ]] || return 1

    local pid=${line[-1]%%/*}
    case $pid in
        *[^0-9]*) findPidByPortApproximately "$port" ;;
        *) echo "$pid" ;;
    esac
}

findPidByPortApproximately() {
    [[ $# == 1 ]] || usage "findPidByPortApproximately port"
    local port=$1; shift

    ps | grep "[ ]$port\>" | awk '{ print $1 }'
}

verifyPort() {
    [[ $# == 1 ]] || usage "verifyPort port"
    local port=$1; shift

    netstat -ntl | grep -q ":$port "
}

waitForPort() {
    [[ $# == 1 ]] || usage "waitForPort port"
    local port=$1; shift

    for _ in 1 2 3; do
        if verifyPort "$port"; then
            return
        fi
        msg "waiting a bit more for port $port to come up ..."
        sleep 1
    done
}

loadConfig() {
    local configfile=.config.sh
    [[ -f "$configfile" ]] || fatal "config file $configfile missing (see $configfile.sample)"
    . "$configfile"
}
