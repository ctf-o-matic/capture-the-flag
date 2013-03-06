#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

mkdir -p $(dirname "$livecd0")

test -f $livecd0 || cmd curl -o $livecd0 $livecd_url

# eof
