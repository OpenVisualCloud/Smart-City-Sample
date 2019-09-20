#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
yml="$DIR/docker-compose.yml"

sudo docker stack rm opnc
