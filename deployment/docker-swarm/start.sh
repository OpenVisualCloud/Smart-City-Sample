#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="$2"
NOFFICES="${NOFFICES:=1}"
PLATFORM="$3"
PLATFORM="${PLATFORM:=Xeon}"
yml="$DIR/docker-compose.yml"

sudo docker container prune -f
sudo docker volume prune -f
sudo docker network prune -f

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

    "$DIR/../certificate/self-sign.sh"
    "$DIR/build.sh" 1 ${PLATFORM}
    export STORAGE_VOLUME=$(readlink -f "$DIR/../../volume/storage")
    test -n "$(ls -A $STORAGE_VOLUME)" && rm -rf "$STORAGE_VOLUME"/*
    sudo -E docker-compose -f "$yml" -p smtc --compatibility up
    ;;
*)
    "$DIR/../certificate/self-sign.sh"
    "$DIR/build.sh" ${NOFFICES} ${PLATFORM}
    if test "${NOFFICES:=1}" -gt 1; then
        export STORAGE_VOLUME="/mnt/storage"
    else
        export STORAGE_VOLUME=$(readlink -f "$DIR/../../volume/storage")
        test -n "$(ls -A $STORAGE_VOLUME)" && rm -rf "$STORAGE_VOLUME"/* || echo
    fi
    sudo -E docker stack deploy -c "$yml" smtc
    ;;
esac
