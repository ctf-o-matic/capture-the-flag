#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

install_tcz gcc_libs openssh openssl-1.0.0

sshd_config=$extract/usr/local/etc/ssh/sshd_config
test -f $sshd_config || cp $sshd_config.example $sshd_config

# eof
