#!/bin/bash

pbf="$1"
if test -z "$pbf"; then
    echo "Usage: pbf"
    exit 3
fi

sudo docker volume rm openstreetmap-data
sudo docker volume create openstreetmap-data
IMAGE="overv/openstreetmap-tile-server:1.1"
sudo docker run -v $(readlink -f "$pbf"):/data.osm.pbf -v openstreetmap-data:/var/lib/postgresql/10/main ${IMAGE} import
sudo docker run -p 8080:80 -v openstreetmap-data:/var/lib/postgresql/10/main -d ${IMAGE} run
