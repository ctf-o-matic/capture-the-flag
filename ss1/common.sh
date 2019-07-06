#!/usr/bin/env bash

_ssh() {
    ssh -p 8022 \
        -oStrictHostKeyChecking=no \
        -oUserKnownHostsFile=/dev/null \
        -oLogLevel=QUIET \
        "$@"
}
