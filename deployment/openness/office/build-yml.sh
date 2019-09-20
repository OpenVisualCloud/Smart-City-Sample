#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
OFFICE=$(echo ${1-eee1} | cut -f4 -d'e')
PLATFORM="${2:-Xeon}"
SCENARIO="${3:-traffic}"
NOFFICES="${4:-1}"
NCAMERAS="${5:-5}"
NANALYTICS="${6:-3}"

if test -f "${DIR}/docker-compose.yml.m4"; then
    echo "Generating docker-compose.yml for office${OFFICE}"
    m4 -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS} -DNANALYTICS=${NANALYTICS} -DOFFICEIDX=${OFFICE} -I "${DIR}" "${DIR}/docker-compose.yml.m4" > "${DIR}/docker-compose.yml"
fi
