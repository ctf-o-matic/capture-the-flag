#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
name=$(basename "$PWD")

docker build -t "$name" .
