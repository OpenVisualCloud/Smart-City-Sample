#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="${4:-1}"
yml="$DIR/docker-compose.yml"


export USER_ID="$(id -u)"
export GROUP_ID="$(id -g)"
case "$1" in
docker_compose)
    dcv="$(docker-compose --version | cut -f3 -d' ' | cut -f1 -d',')"
    mdcv="$(printf '%s\n' $dcv 1.20 | sort -r -V | head -n 1)"
    if test "$mdcv" = "1.20"; then
        echo ""
        echo "docker-compose >=1.20 is required."
        echo "Please upgrade docker-compose at https://docs.docker.com/compose/install."
        echo ""
        exit 0
    fi

    echo "Cleanup..."
    docker volume prune -f; echo

    "$DIR/../certificate/self-sign.sh"
    shift
    . "$DIR/build.sh"
    docker-compose -f "$yml" -p smtc --compatibility up
    ;;
*)
    echo "Cleanup..."
    $DIR/../../script/cleanup.sh; echo

    "$DIR/../certificate/self-sign.sh"
    shift
    . "$DIR/build.sh"
    docker stack deploy -c "$yml" smtc
    ;;
esac
