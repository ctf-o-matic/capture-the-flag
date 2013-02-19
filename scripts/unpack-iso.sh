#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

mkdir -p $mnt

if ! ls $squashfs >/dev/null 2>/dev/null; then
    mount | grep $livecd0 >/dev/null || cmd sudo mount $livecd0 $mnt
    cmd mkdir -p $newiso
    cmd rsync -av $mnt/* $newiso/
    cmd sudo umount $livecd0
fi

# eof
