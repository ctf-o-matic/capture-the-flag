#!/usr/bin/env bash

msg() {
    echo "* $@"
}

waitForPort() {
    local port=$1
    for _ in 1 2 3; do
        netstat -ntl | grep -q "$port " && {
            msg "port $port is up"
            return
        }
        msg "waiting a bit more for port $port to come up ..."
        sleep 1
    done

    msg "port $port is NOT up"
}

./start-ssh-server.sh

#waitForPort 22
#waitForPort 8002
#waitForPort 8004

netstat -ntl
