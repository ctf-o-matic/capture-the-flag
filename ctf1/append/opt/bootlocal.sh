#!/bin/sh
LOGDIR=/var/log
(/usr/local/etc/init.d/openssh start >>$LOGDIR/custom-sshd.log 2>&1)&
(exec sudo -u level02 /home/level02/start.sh >> $LOGDIR/level02.log 2>&1)&
(exec sudo -u level05 /home/level05/start.sh >> $LOGDIR/level05.log 2>&1)&
