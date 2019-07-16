#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

. ./setup/common.sh
. ./common.sh

if [[ $# = 1 ]]; then
    host=$1; shift
else
    host=localhost
fi

as_root() {
    _ssh "root@$host" "$@"
}

test_recover_from_corrupted_file() {
    local user_file=$1; shift
    local orig_file=$1; shift

    as_root << EOF
set -euo pipefail

cmp "$user_file" "$orig_file"

rm -v "$user_file"
/setup/reset.sh "$level" --skip-service
cmp "$user_file" "$orig_file"

date >> "$user_file"
/setup/reset.sh "$level" --skip-service
cmp "$user_file" "$orig_file"

chmod 0 "$user_file"
/setup/reset.sh "$level" --skip-service
cmp "$user_file" "$orig_file"
EOF
}

test_recover_from_corrupted_file_if_exists() {
    local user_file=$1; shift
    local orig_file=$1; shift

    if as_root "[[ -f '$user_file' ]] && [[ -f '$orig_file' ]]"; then
        test_recover_from_corrupted_file "$user_file" "$orig_file"
    fi
}

test_recover_from_corrupted_permission() {
    local user_path=$1; shift
    local permission=$1; shift

    as_root << EOF
set -euo pipefail

pcmp() {
    local path=\$1; shift
    local perm=\$1; shift
    local p=\$(ls -ld "\$path" | awk '{ print \$1 }')
    [[ "\$p" == "\$perm" ]]
}

pcmp "$user_path" "$permission"

chmod 0 "$user_path"
/setup/reset.sh "$level" --skip-service
pcmp "$user_path" "$permission"

chmod 7777 "$user_path"
/setup/reset.sh "$level" --skip-service
pcmp "$user_path" "$permission"
EOF
}

test_recover_from_corrupted_permission_if_exists() {
    local user_path=$1; shift
    local permission=$1; shift

    if as_root "[[ -f '$user_path' ]] || [[ -d '$user_path' ]]"; then
        test_recover_from_corrupted_permission "$user_path" "$permission"
    fi
}

test_recover_from_corrupted_service() {
    local level=$1; shift
    local port=$(levelport "$level")

    as_root << EOF
set -euo pipefail

/setup/service.sh "$level" stop || :
! /setup/service.sh "$level" status

/setup/service.sh "$level" restart
/setup/service.sh "$level" status
EOF
}

test_recover_from_corrupted_service_if_exists() {
    local level=$1; shift

    if as_root "[[ -f '/var/run/levels/$level/start.sh' ]]"; then
        test_recover_from_corrupted_service "$level"
    fi
}

for leveldir in levels/level?/; do
    level=$(basename "$leveldir")
    msg "testing reset for $level ..."

    test_recover_from_corrupted_file "/home/$level/.password" "/setup/generated/levels/$level/home/.password"
    test_recover_from_corrupted_file "/home/$level/.profile" "/setup/generated/levels/$level/home/.profile"
    test_recover_from_corrupted_permission "/home/$level" 'drwx------'

    [[ "$level" != "level0" ]] || continue

    test_recover_from_corrupted_file_if_exists "/levels/$level/prog" "/setup/generated/levels/$level/special/prog"

    test_recover_from_corrupted_permission_if_exists "/levels/$level/prog" '-r-sr-xr-x'
    test_recover_from_corrupted_permission "/levels/$level" 'drwxr-x---'
    test_recover_from_corrupted_permission "/var/run/levels/$level/wwwdata" 'drwx------'

    test_recover_from_corrupted_service_if_exists "$level"
done
