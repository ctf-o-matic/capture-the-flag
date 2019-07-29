#!/usr/bin/env bash
#
# Usage:
#
# 1. Put this script somewhere in your project
#
# 2. Edit crontab.txt file, it should look like this,
#    except the # in front of the lines
#
#0 * * * * stuff_you_want_to_do
#15 */5 * * * stuff_you_want_to_do
#* * 1,2 * * and_so_on
#
# 3. To install the crontab, simply run this script
#
# 4. To remove the crontab, run ./crontab.sh --remove
# 

cd "$(dirname "$0")"

set -euo pipefail

usage() {
    local exitcode=0
    if [[ $# != 0 ]]; then
        echo "$*" >&2
        exitcode=1
    fi

    cat << EOF
Usage: $0 [OPTIONS]...

Install or remove the crontab setting defined in crontab.txt file.

Options:
      --remove       Remove the crontab
  -h, --help         Print this help

EOF
    exit "$exitcode"
}

fatal() {
    echo "Error: $*" >&2
    exit 1
}

msg() {
    echo "* $*"
}

crontab_exists() {
    crontab -l 2>/dev/null | grep -qx "$cron_unique_label"
}

backup_crontab() {
    local crontab_bak=./crontab.bak

    msg "Creating backup of current crontab in $crontab_bak ..."
    crontab -l > "$crontab_bak" || :
}

expand_select_vars() {
    sed -e 's?$PWD?'"$PWD"'?g'
}

install_crontab() {
    if crontab_exists; then
        msg "Crontab entry already exists, skipping ..."
        echo
        msg "To remove it, run: $0 --remove"
        echo
        return
    fi

    backup_crontab

    msg "Appending to crontab:"
    {
        echo
        sed -e 's/^/  /' | expand_select_vars
        echo
    } < "$crontab_txt"

    {
        crontab -l 2>/dev/null
        echo "$cron_unique_label"
        cat "$crontab_txt" | expand_select_vars
        echo
    } | crontab -

    msg "To remove it later, run: $0 --remove"
    echo
}

remove_crontab() {
    if crontab_exists; then
        backup_crontab
        msg "Removing crontab entry ..."
        crontab -l 2>/dev/null | sed -e "\?^$cron_unique_label\$?,/^\$/ d" | crontab -
    else
        msg "Crontab entry does not exist, nothing to do."
    fi
}

type crontab &>/dev/null || fatal "it seems the crontab command does not exist (not on PATH). Abort."

mode=install
while [[ $# != 0 ]]; do
    case $1 in
    -h|--help) usage ;;
    --remove) mode=remove ;;
    -|-?*) usage "Unknown option: $1" ;;
    *) usage "Unexpected arguments: $*" ;;
    esac
    shift
done

crontab_txt=./crontab.txt
[[ -f "$crontab_txt" ]] || fatal "crontab definition file does not exist: $crontab_txt"

cron_unique_label="# $PWD"

if [[ "$mode" == install ]]; then
    install_crontab
elif [[ "$mode" == remove ]]; then
    remove_crontab
fi
