#!/usr/bin/env bash

set -euo pipefail

rc-status
touch /run/openrc/softlevel
openrc -s sshd start
