#!/usr/bin/env bash

set -euo pipefail

msg() {
    echo "[*] $*"
}

cmd() {
    echo "[cmd] $*"
    "$@"
}

fatal() {
    echo "[fatal] $*"
    exit 1
}
