#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
yml="$DIR/docker-compose.yml"

    docker stack rm smtc
