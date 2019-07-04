#!/usr/bin/env bash
#
# Helper script to iterate fast
#

set -euo pipefail

./configure.sh
./build.sh
./run.sh bash

# tip: test a new level with: ./crack.sh level0X
