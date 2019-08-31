#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
NOFFICES="${2:-1}"
NCAMERAS="${3:-5}"
NSERVICES="${4:-3}"

if test -f "${DIR}/docker-compose.yml.m4"; then
    echo "Generating docker-compose.yml with NOFFICES=${NOFFICES} and PLATFORM=${PLATFORM}"
    m4 -DNOFFICES=${NOFFICES} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS} -DNSERVICES=${NSERVICES} -I "${DIR}" "${DIR}/docker-compose.yml.m4" > "${DIR}/docker-compose.yml"
fi
