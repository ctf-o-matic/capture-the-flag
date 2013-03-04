#!/bin/sh -e
#
# File:
# Purpose:
#

cd $(dirname "$0"); . ./common.sh; cd ..

install_tcz openssh

exit_if_nonroot

sshd_config=$extract/usr/local/etc/ssh/sshd_config
test -f $sshd_config || cp $sshd_config.example $sshd_config

# eof
