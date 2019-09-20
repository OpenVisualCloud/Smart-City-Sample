#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
OFFICE=$(echo ${1-eee1} | cut -f4 -d'e')
yml="$DIR/docker-compose.yml"

sudo docker container prune -f
sudo docker volume prune -f
sudo docker network prune -f

export USER_ID="$(id -u)"
export GROUP_ID="$(id -g)"

. "$DIR/build-yml.sh"

if test -z "$CLOUDHOST"; then
    export CLOUDHOST="$(hostname -i)"
fi
if test -z "$CAMERAHOST"; then
    export CAMERAHOST="$(hostname -i)"
fi
sudo -E docker stack deploy -c "$yml" opncam
