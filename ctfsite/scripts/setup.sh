#!/bin/sh

cd "$(dirname "$0")"/..

venv=./venv
test -d "$venv" || python3 -m venv "$venv"

requirements=requirements.txt
test -f "$requirements" && ./pip.sh install -r "$requirements" || :
