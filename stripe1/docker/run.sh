#!/usr/bin/env bash

docker run -it --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    -p 8022:22 -p 8002:8002 -p 8005:8005 \
    stripe1
