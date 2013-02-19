#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

tmp=squashfs.gz
{ cd $extract; sudo find | cmd sudo cpio -o -H newc; } | gzip -2 > $tmp
cmd advdef -z4 $tmp
cmd sudo mv $tmp $squashfs
cmd sudo mkisofs -l -J -R -V TC-custom -no-emul-boot -boot-load-size 4 \
    -boot-info-table -b boot/isolinux/isolinux.bin \
    -c boot/isolinux/boot.cat -o $livecd1 $newiso

# eof
