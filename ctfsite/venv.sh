#!/usr/bin/env bash

venv=$(dirname "$BASH_SOURCE")/venv
if test -d "$venv"; then
    . "$venv"/bin/activate
else
    {
        echo "venv does not exist: $venv"
        echo "Create it with: ./scripts/setup.sh"
    } >&2
    exit 1
fi
