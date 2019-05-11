#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

sudo ./scripts/clean.sh

./scripts/build.sh

sudo ./scripts/pack-iso.sh

# eof
