#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

exit_if_nonroot

if ! ls $extract/proc >/dev/null 2>/dev/null; then
    cmd mkdir -p $extract
    zcat $squashfs | { cd $extract; cpio -i -H newc -d; }
fi

# eof
