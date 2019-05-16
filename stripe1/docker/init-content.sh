#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

for home in static-files/home/level*; do
    username=${home##*/}
    generated_home=generated-files/home/$username
    mkdir -p "$generated_home"

    password=$(pwgen 8 1)
    echo "$password" > "$generated_home/.password"

    {
        cat helper-files/motd/banner.txt
        cat "helper-files/motd/levels/$username.txt"
    } > "$generated_home/motd.txt"

    cp helper-files/.profile "$generated_home"
done
