#!/usr/bin/env bash

cd "$(dirname "$0")"

set -euo pipefail

cd "$(dirname "$0")"
backups_dir=./backups

usage() {
    local exitcode=0
    if [[ $# != 0 ]]; then
        echo "$*" >&2
        exitcode=1
    fi

    cat << EOF
Usage: $0 [OPTIONS]... [hourly|daily|weekly|monthly] [files]...

Backup specified files periodically as simple copy + gzip.

Options:
  -h, --help         Print this help

EOF
    exit "$exitcode"
}

fatal() {
    echo "Error: $*" >&2
    exit 1
}

msg() {
    echo "* $*"
}

args=()
while [[ $# != 0 ]]; do
    case $1 in
    -h|--help) usage ;;
    -|-?*) usage "Unknown option: $1" ;;
    *) args+=("$1") ;;
    esac
    shift
done

set -- "${args[@]}"

if (( $# < 2 )); then
    usage
fi

period=$1; shift

backup() {
    local suffix=$1; shift
    local src dst
    for src; do
        if ! [[ -f "$src" ]]; then
            msg "skipping not regular file: $src"
            continue
        fi
        mkdir -p "$backups_dir"
        dst=$backups_dir/$(basename "$src").$suffix
        cp -v "$src" "$dst"
        gzip -vf "$dst"
    done
}

case $period in
    hourly) backup "$(date +%H)" "$@" ;;
    daily) backup "$(date +%a)" "$@" ;;
    weekly) backup "$(date +%d)" "$@" ;;
    monthly) backup "$(date +%b)" "$@" ;;
    *) usage
esac
