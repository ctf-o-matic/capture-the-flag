#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. common.sh

username=$1; shift
_ssh "$username@localhost" "$@"
