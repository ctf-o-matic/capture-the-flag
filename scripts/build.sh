#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

./scripts/get-livecd.sh

./scripts/get-ctf1.sh

sudo ./scripts/unpack-iso.sh

sudo ./scripts/unpack-squashfs.sh

sudo ./scripts/setup-ctf1.sh

# eof
