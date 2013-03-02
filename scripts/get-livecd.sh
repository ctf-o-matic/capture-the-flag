#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

test -f $livecd0 || cmd curl -o $livecd0 $livecd_url

# eof
