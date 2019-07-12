#!/usr/bin/env bash

set -euo pipefail

. /setup/common.sh

_usage() {
    [[ $# = 0 ]] || error "$@"
    usage "$0: level <start|stop|restart|status>"
}

[[ $# = 2 ]] || _usage

level=$1; shift
cmd=$1; shift

is_valid_cmd() {
    case $1 in
        start|stop|restart|status) ;;
        *) return 1
    esac
}

is_valid_level "$level" || _usage "not a valid level: $level"

start_script=/var/run/levels/$level/start.sh
[[ -x "$start_script" ]] || _usage "not a valid level, start script missing: $start_script"

is_valid_cmd "$cmd" || _usage "not a valid command: $cmd"

rundir=/var/run/levels/$level

logdir=/var/log
logfile=$logdir/$level.log

port=$(levelport "$level")

status() {
    if verifyPort "$port"; then
        msg "port $port is up"
        return
    else
        msg "port $port is down"
        return 1
    fi
}

start() {
    if status; then
        return
    fi

    local pids=($(findPidByPort "$port"))
    if [[ ${#pids[@]} != 0 ]]; then
        local pid
        for pid in "${pids[@]}"; do
            msg "port appears to be up by process $pid -> killing it ..."
            kill -9 "$pid"
        done
        sleep 1
    fi

    msg "starting process for $level ..."

    (sudo -u "$level" "$start_script" "$rundir" "$port" &>> "$logfile")&

    waitForPort "$port"
    status
}

stop() {
    if ! status; then
        return
    fi

    local pids=($(findPidByPort "$port"))
    if [[ ${#pids[@]} != 0 ]]; then
        local pid
        for pid in "${pids[@]}"; do
            msg "stopping process $pid running service listening on port $port ..."
            kill -9 "$pid"
        done
        sleep 1
    fi
    status
}

restart() {
    stop || :
    start
}

"$cmd"
