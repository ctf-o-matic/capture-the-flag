#!/usr/bin/env bash
#
# Delete .password files in the generated content
#

set -euo pipefail

cd "$(dirname "$0")"

generated=setup/generated

find "$generated" -name .password -ls -delete
