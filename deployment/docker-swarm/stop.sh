#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
yml="$DIR/docker-compose.yml"

case "$1" in
docker_compose)
    dcv="$(docker-compose --version | cut -f3 -d' ' | cut -f1 -d',')"
    mdcv="$(printf '%s\n' $dcv 1.10 | sort -r -V | head -n 1)"
    if test "$mdcv" = "1.10"; then
        echo ""
        echo "docker-compose >=1.10 is required."
        echo "Please upgrade docker-compose at https://docs.docker.com/compose/install."
        echo ""
        exit 0
    fi
    docker-compose -f "$yml" -p smtc --compatibility down
    ;;
*)
    docker stack rm smtc
    ;;
esac
