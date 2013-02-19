#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

test -d $ctf1 || cmd git clone https://github.com/stripe-ctf/stripe-ctf $ctf1

# eof
