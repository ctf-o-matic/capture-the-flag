#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

exit_if_nonroot

tcz_url=http://distro.ibiblio.org:/tinycorelinux/4.x/x86/tcz
packages='gcc_libs openssh openssl-1.0.0'
tcz_dir=./tcz

mkdir -p $tcz_dir

for package in $packages; do
    target=$tcz_dir/$package.tcz
    test -f $target || curl -o $target $tcz_url/$package.tcz
    tce_marker=$extract/usr/local/tce.installed/$package
    if ! test -f $tce_marker; then
        unsquashfs -f -d $extract $target
        touch $tce_marker
    fi
done

sshd_config=$extract/usr/local/etc/ssh/sshd_config
test -f $sshd_config || cp $sshd_config.example $sshd_config

# eof
