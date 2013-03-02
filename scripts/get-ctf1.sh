#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

test -d $ctf1_orig || cmd git clone https://github.com/stripe-ctf/stripe-ctf $ctf1_orig

# eof
