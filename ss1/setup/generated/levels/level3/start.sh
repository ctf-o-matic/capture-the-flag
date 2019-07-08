#!/usr/bin/env bash

set -euo pipefail

rundir=$1; shift
port=$1; shift

cd "$rundir"
# TODO something's broken, should work with ./tmp/wwwdata
PYTHONPATH=./runtime ./code/prog.py "$port" /tmp/wwwdata server &
PYTHONPATH=./runtime ./code/prog.py "$port" /tmp/wwwdata worker &

wait
