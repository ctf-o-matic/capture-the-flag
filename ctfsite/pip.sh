#!/usr/bin/env bash

cd "$(dirname "$0")"
. ./venv.sh

pip "$@"
