#!/bin/bash

pbf="$1"
if test -z "$pbf"; then
    echo "Usage: pbf"
    exit 3
fi

docker volume rm openstreetmap-data
docker volume create openstreetmap-data
IMAGE="overv/openstreetmap-tile-server:1.1"
docker run -v $(readlink -f "$pbf"):/data.osm.pbf -v openstreetmap-data:/var/lib/postgresql/10/main ${IMAGE} import
docker run -p 8080:80 -v openstreetmap-data:/var/lib/postgresql/10/main -d ${IMAGE} run
