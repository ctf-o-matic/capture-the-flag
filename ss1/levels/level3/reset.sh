#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

level=$(basename "$PWD")

# TODO move all this to init and common reset and delete this file
rundir=/var/run/levels/$level

rm -fr "$rundir"
mkdir "$rundir"

cp -vr code "$rundir/code"
cp -v start.sh "$rundir"

mkdir -p "$rundir/wwwdata"
chmod 700 "$rundir/wwwdata"
chown "$level" "$rundir/wwwdata"

if [[ $# == 0 ]]; then
    /setup/service.sh "$level" restart
fi
