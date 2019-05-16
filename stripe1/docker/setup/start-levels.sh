#!/usr/bin/env bash

set -euo pipefail

logdir=/var/log

msg() {
    echo "* $@"
}

for home in /home/level*; do
    msg "checking if start script exists in $home"

    script=$home/start.sh
    [ -x "$script" ] || continue

    msg "start script detected: $script"

    user=${home##*/}
    logfile=$logdir/$user.log
    pidfile=$logdir/$user.pid

    if [ -f "$pidfile" ]; then
        msg "pid file detected: $pidfile"
        pid=$(cat "$pidfile")
        if kill -0 "$pid" &>/dev/null; then
            msg "pid $pid appears to be up for $user"
            continue
        fi
    fi

    msg "starting process for user $user"

    (exec sudo -u "$user" $home/start.sh &>> "$logfile")&
    pid=$!
    echo "$pid" > "$pidfile"

    msg "started process for user $user, PID $pid stored in $pidfile"
done
