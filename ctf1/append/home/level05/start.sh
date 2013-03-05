#!/bin/sh

cd $(dirname "$0")
PYTHONPATH=. /levels/level05/level05.py server &
PYTHONPATH=. /levels/level05/level05.py worker &
