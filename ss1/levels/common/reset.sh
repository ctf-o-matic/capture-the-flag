#!/usr/bin/env bash
#
# common setup for a level:
# - copy common files, such as .profile
# - fix owner of home dir
# - fix permissions on home dir

set -euo pipefail

level=$1; shift

cd "$(dirname "$0")"

home_src=../$level/home
home_dst=/home/$level

[[ -d "$home_dst" ]]

cp -v home/.??* "$home_dst"
cp -v home/* "$home_dst" || :
cp -v "$home_src"/.??* "$home_dst"
cp -v "$home_src"/* "$home_dst"
chown -Rv "$level:$level" "$home_dst"
chmod -v 0700 "$home_dst"

code_src=../$level/code
code_dst=/levels/$level

if [[ -d "$code_src" ]]; then
    mkdir -p "$code_dst"
    cp -Rv "$code_src"/* "$code_dst"
    chown -Rv "$level:$level" "$code_dst"
    chmod -Rv g-w,o-rwx "$code_dst"
fi

rundir=/var/run/levels
mkdir -p "$rundir"
chmod 701 "$rundir"
