#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"
name=$(basename "$PWD")

port_args=(-p 8022:22)
for ((i = 1; i <= 8; i++)); do
    ((port = 8000 + i))
    port_args+=(-p "$port")
done

docker run -it --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    "${port_args[@]}" \
    "$name" "$@"
