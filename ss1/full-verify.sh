#!/usr/bin/env bash
#
# Helper script to iterate fast
#

set -euo pipefail

if ./configure.sh && ./build.sh && ./run-tests.sh; then
    echo "SUCCESS"
else
    echo "FAILED"
fi
