#!/usr/bin/env bash

set -euo pipefail

rundir=$1; shift
port=$1; shift

cd "$rundir"
php7 -S "0.0.0.0:$port" -t code
