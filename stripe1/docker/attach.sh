#!/usr/bin/env bash

echo "Detach without stopping the container with ^P^Q"

container_id=$(docker ps -q -l -f ancestor=stripe1)

echo "Attempting to attach to container: $container_id"

docker attach "$container_id"
