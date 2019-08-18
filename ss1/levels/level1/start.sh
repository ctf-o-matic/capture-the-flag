#!/usr/bin/env bash

set -euo pipefail

rundir=$1; shift
port=$1; shift

cd "$rundir"
PYTHONPATH=./runtime ./code/prog.py "$port" ./wwwdata
