#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="$1"
NOFFICES="${NOFFICES:=1}"
PLATFORM="$2"
PLATFORM="${PLATFORM:=Xeon}"

if test -f "${DIR}/docker-compose.yml.m4"; then
    echo "Generating docker-compose.yml with NOFFICES=${NOFFICES} and PLATFORM=${PLATFORM}"
    m4 -DNOFFICES=${NOFFICES} -DPLATFORM=${PLATFORM} -I "${DIR}" "${DIR}/docker-compose.yml.m4" > "${DIR}/docker-compose.yml"
fi
