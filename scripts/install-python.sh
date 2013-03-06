#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

install_tcz python

exit_if_nonroot

rm -f $extract/usr/local/share/python/files/files.tar.gz

# eof
