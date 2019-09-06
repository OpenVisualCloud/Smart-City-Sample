#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NODEIP="172.32.1.1"
NODEUSER="root"

YML="${DIR}/../deployment/docker-swarm/docker-compose.yml"
for image in $(awk '/command:/{im=$NF;gsub(/\"/,"",im)}/vcac_zone==yes/{print im}' "$YML"); do
    echo "Transfer image: $image"
    sudo docker save $image | ssh $NODEUSER@$NODEIP "docker image rm -f $image 2>/dev/null; docker load"
done
