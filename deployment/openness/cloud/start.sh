#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="${4:-1}"
yml="$DIR/docker-compose.yml"

export USER_ID="$(id -u)"
export GROUP_ID="$(id -g)"
"$DIR/../../certificate/self-sign.sh"
sudo -E docker stack deploy -c "$yml" opnc
