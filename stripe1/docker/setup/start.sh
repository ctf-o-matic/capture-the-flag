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

./start-levels.sh

waitForPort 22
waitForPort 8002
waitForPort 8004

netstat -ntl

# TODO make sure that solutions are excluded from production builds
if [ -d ./solutions ]; then
    for script in ./solutions/*.sh; do
        "$script"
    done
fi

bash
