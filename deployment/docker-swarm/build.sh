#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="$1"

if test -f "${DIR}/docker-compose.yml.m4"; then
    echo "Generating docker-compose.yml with NOFFICES=${NOFFICES:=1}"
    m4 -DNOFFICES=${NOFFICES:=1} -I "${DIR}" "${DIR}/docker-compose.yml.m4" > "${DIR}/docker-compose.yml"
fi
