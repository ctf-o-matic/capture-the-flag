#!/usr/bin/env bash

bytes=$(docker image inspect stripe1:latest --format='{{.Size}}')

echo "$((bytes / 1024 / 1024))"
