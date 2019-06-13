#!/usr/bin/env bash

docker run -it --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    -p 8022:22 -p 8002:8002 -p 8004:8004 \
    stripe1
