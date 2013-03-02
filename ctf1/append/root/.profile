#!/bin/sh
INIT=/tmp/INIT
if ! test -f $INIT; then
    /usr/local/etc/init.d/openssh start > $INIT
fi
exec /bin/login -f level00
