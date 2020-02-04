#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
yml="$DIR/docker-compose.yml"

docker stack services smtc
echo "Shutting down stack smtc..."
while test -z "$(docker stack rm smtc 2>&1 | grep 'Nothing found in stack')"; do
    sleep 2
done
