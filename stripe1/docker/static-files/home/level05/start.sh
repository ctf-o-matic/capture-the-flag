#!/usr/bin/env bash

cd "$(dirname "$0")"
PYTHONPATH=. /levels/level05/level05.py server &
PYTHONPATH=. /levels/level05/level05.py worker &

wait
