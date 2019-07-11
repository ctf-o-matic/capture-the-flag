#!/usr/bin/env bash
#
# Configure the content based on levels:
# - copy files to setup
# - generate .password
#

set -euo pipefail

cd "$(dirname "$0")"
. setup/common.sh

generated=setup/generated
rm -fr "$generated"

# directories matching "level?"
levels=(levels/level?/)
# strip trailing "/"
levels=(${levels[@]%/})
# strip beginning, leaving only the directory name
levels=(${levels[@]##*/})

create_password() {
    pwgen 16 1
}

create_welcome_message() {
    local current=$1; shift
    local next=$1; shift
    local src=$1; shift
    local dst=$1; shift
    local output=$dst/home/message.txt

    msg "creating message file: $output ..."

    local current_level_num=$(num "$current")
    local next_level_port=$(levelport "$current")
    ((next_level_port++))

    if [[ "$current_level_num" == "0" ]]; then
        cat messages/banner.txt messages/first.txt > "$output"
        cp -v messages/*-help.txt "$dst/home/"
    elif ! [[ "$next" ]]; then
        cat messages/banner.txt messages/last.txt > "$output"
    else
        local hintfile=levels/$next/hint.tpl
        cat messages/banner.txt messages/middle.tpl | \
        sed -e "/__HINT__/r $hintfile" -e "/__HINT__/d" | \
        sed \
            -e "s/__CURRENT_LEVEL_NUM__/$current_level_num/g" \
            -e "s/__NEXT_LEVEL_PORT__/$next_level_port/g" \
            -e "s/__NEXT_LEVEL__/$next/g" \
            > "$output"
    fi
}

create_level() {
    local current=$1
    local next=$2
    local src=levels/$current
    local dst=$generated/levels/$current

    msg "creating level: $current ..."

    # TODO copy common home files, instead of doing that in reset.sh
    mkdir -p "$dst/home"
    for dirname in home code special runtime; do
        [[ -d "$src/$dirname" ]] && cp -vr "$src/$dirname/" "$dst/$dirname"
    done
    for filename in reset.sh start.sh; do
        [[ -f "$src/$filename" ]] && cp -v "$src/$filename" "$dst/"
    done

    create_password > "$dst/home/.password"
    create_welcome_message "$current" "$next" "$src" "$dst"
}

for ((i = 0; i < ${#levels[@]} - 1; i++)); do
    current=${levels[i]}
    next=${levels[i+1]}

    create_level "$current" "$next"
done

create_level "${levels[i]}" ""

msg "copy common files ..."
cp -rv levels/common "$generated"/levels/

msg "setup root user and authorized ssh keys ..."
mkdir -p "$generated"/root/.ssh
ssh-add -L > "$generated"/root/.ssh/authorized_keys
create_password > "$generated"/root/.password
chmod -R go-rwx "$generated"/root
