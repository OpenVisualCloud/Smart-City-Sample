#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
#yml="$DIR/docker-compose.yml"
#sudo docker-compose -f "$yml" -p opncam --compatibility down

for id in $(sudo docker ps | grep smtc_sensor_simulation | cut -f1 -d" "); do
    echo $id
    sudo -E docker kill $id
done
