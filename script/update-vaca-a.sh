#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NODEIP="172.32.1.1"
NODEUSER="root"

YML="${DIR}/../deployment/docker-swarm/docker-compose.yml"
for image in $(awk '/command:/{im=$NF;gsub(/\"/,"",im)}/vcac_zone==yes/{print im}' "$YML"); do
    echo "Transfer image: $image"
    signature1=$(sudo docker image inspect -f {{.ID}} $image)
    echo " local: $signature1"
    signature2=$(ssh $NODEUSER@$NODEIP "docker image inspect -f {{.ID}} $image 2> /dev/null || echo")
    echo "remote: $signature2"
    if test "$signature1" != "$signature2"; then
        sudo docker save $image | ssh $NODEUSER@$NODEIP "docker image rm -f $image 2>/dev/null; docker load"
    fi
done
