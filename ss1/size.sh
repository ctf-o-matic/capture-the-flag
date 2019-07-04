#!/usr/bin/env bash

set -euo pipefail

name=$(basename "$PWD")
bytes=$(docker image inspect "$name:latest" --format='{{.Size}}')

echo "$((bytes / 1024 / 1024))"
