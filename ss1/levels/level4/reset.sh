#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

level=$(basename "$PWD")

cd "/var/run/levels/$level/code"
rm -fr wwwdata
mkdir wwwdata
chown -v "$level:$level" wwwdata
chmod -v 0700 wwwdata
