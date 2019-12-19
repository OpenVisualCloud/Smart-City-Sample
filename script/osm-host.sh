#!/bin/bash

pbf="$1"
if test -z "$pbf"; then
    echo "Usage: pbf"
    exit 3
fi

docker volume rm openstreetmap-data
docker volume rm openstreetmap-nodes
docker volume create openstreetmap-data
docker volume create openstreetmap-nodes
IMAGE="overv/openstreetmap-tile-server:1.3.8"
docker run --rm $(env | grep -E '_(proxy)=' | sed 's/^/-e /') -v $(readlink -f "$pbf"):/data.osm.pbf -v openstreetmap-nodes:/nodes -v openstreetmap-data:/var/lib/postgresql/12/main -e "OSM2PGSQL_EXTRA_ARGS=--flat-nodes /nodes/flat_nodes.bin" ${IMAGE} import
docker run --rm -p 8080:80 -v openstreetmap-data:/var/lib/postgresql/12/main --shm-size="192m" -d ${IMAGE} run
