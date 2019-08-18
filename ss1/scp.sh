#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
. common.sh

_scp "$@"
