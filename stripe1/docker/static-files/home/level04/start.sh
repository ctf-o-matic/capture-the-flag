#!/usr/bin/env bash

cd "$(dirname "$0")"
PYTHONPATH=. /levels/level04/level04.py server &
PYTHONPATH=. /levels/level04/level04.py worker &

wait
