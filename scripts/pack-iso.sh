#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

exit_if_nonroot

# add build info
printf '\n%60s\n' "$(date)" > $build_info
printf '%60s\n\n' "$(git rev-list HEAD -n1)" >> $build_info
boot_msg0=boot/isolinux/boot.msg
cat $ctf1/$boot_msg0 $build_info > $newiso/$boot_msg0

# detect mkisofs executable, name genisoimage in debian
mkisofs=$(which mkisofs genisoimage blah | head -n 1)

tmp=$work/squashfs.gz
{ cd $extract; find | cpio -o -H newc; } | gzip -2 > $tmp
cmd advdef -z4 $tmp
cmd mv $tmp $squashfs
cmd $mkisofs -l -J -R -V TC-custom -no-emul-boot -boot-load-size 4 \
    -boot-info-table -b boot/isolinux/isolinux.bin \
    -c boot/isolinux/boot.cat -o $livecd1 $newiso

msg creating $livecd1.md5
md5sum $livecd1 > $livecd1.md5

msg creating $livecd1.info
(cd $extract; grep . home/*/.password) > $livecd1.info

# eof
