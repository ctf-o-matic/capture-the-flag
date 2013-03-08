#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

exit_if_nonroot

mkdir -pv $mnt

if ! ls $squashfs >/dev/null 2>/dev/null; then
    mount | grep $livecd0 >/dev/null || cmd mount $livecd0 $mnt
    cmd mkdir -p $newiso
    cmd rsync -av $mnt/* $newiso/
    cmd umount $mnt
fi

# eof
