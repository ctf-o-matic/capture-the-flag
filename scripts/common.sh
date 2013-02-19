#!/bin/sh
#
# File: common.sh
# Purpose: common configuration and shell functions
#

livecd0=./livecd.iso
livecd1=./remastered.iso
mnt=./mnt
extract=./extract
newiso=./newiso
squashfs=$newiso/boot/core.gz
ctf1=./ctf1

msg() {
    echo '[*]' $*
}

cmd() {
    echo '[cmd]' $*
    $*
}

error() {
    echo '[E]' $*
    exit 1
}

for i in "$@"; do
    case "$i" in
        -h|--help) usage ; exit 1 ;;
    esac
done

# eof
