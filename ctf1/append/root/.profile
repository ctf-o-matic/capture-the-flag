#!/bin/sh
INIT=/tmp/INIT
if ! test -f $INIT; then
    touch $INIT
    /usr/local/etc/init.d/openssh start
fi
exec /bin/login -f level00
