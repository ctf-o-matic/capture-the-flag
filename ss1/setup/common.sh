#!/usr/bin/env bash

usage() {
    echo "Usage: $@"
    exit 1
}

msg() {
    echo "* $@"
}

cmd() {
    echo "[cmd] $@"
    "$@"
}

error() {
    echo "[error] $@" >&2
}

fatal() {
    echo "[fatal] $@" >&2
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
