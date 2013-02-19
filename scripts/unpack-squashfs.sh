#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

if ! ls $extract/proc >/dev/null 2>/dev/null; then
    cmd mkdir -p $extract
    zcat $squashfs | { cd $extract; sudo cpio -i -H newc -d; }
fi

# eof
