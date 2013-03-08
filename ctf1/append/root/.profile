#!/bin/sh
INIT=/tmp/INIT
if ! test -f $INIT; then
    /usr/local/etc/init.d/openssh start >> $INIT.log
    (exec sudo -u level02 /home/level02/start.sh >> $INIT.log 2>&1)&
    (exec sudo -u level05 /home/level05/start.sh >> $INIT.log 2>&1)&
    touch $INIT
fi
exec /bin/login -f level00
