#!/usr/bin/env bash

usage() {
    echo "Usage: $@"
    exit 1
}

msg() {
    echo "[*] $@"
}

cmd() {
    echo "[cmd] $@"
    "$@"
}

fatal() {
    echo "[fatal] $@"
    exit 1
}
