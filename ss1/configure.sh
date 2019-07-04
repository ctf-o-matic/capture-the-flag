#!/usr/bin/env bash
#
# Configure the content based on levels:
# - copy files to setup
# - generate .password
#

set -euo pipefail

cd "$(dirname "$0")"

generated=setup/generated
rm -fr "$generated"

# directories matching "level*"
levels=(levels/level*/)
# strip trailing "/"
levels=(${levels[@]%/})
# strip beginning, leaving only the directory name
levels=(${levels[@]##*/})

msg() {
    echo "* $@"
}

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

    local commands=()
    if [[ "$next" ]]; then
        hintfile=levels/$next/hint.tpl
        commands+=(sed)
        commands+=(-e "/__HINT__/r $hintfile")
        commands+=(-e "/__HINT__/d")
    else
        commands+=(cat)
    fi

    "${commands[@]}" "$src/message.tpl" \
        | sed -e "s/__LEVEL__/$next/g" \
        > "$output"
}

create_level() {
    local current=$1
    local next=$2
    local src=levels/$current
    local dst=$generated/levels/$current

    msg "creating level: $current ..."

    mkdir -p "$dst/home"
    cp -rv "$src"/ "$dst"/

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
