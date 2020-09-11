#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

docker stack deploy -c "$DIR/docker-compose.yml" smtc
