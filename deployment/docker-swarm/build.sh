#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-traffic}"
NOFFICES="${3:-1}"
IFS="," read -r -a NCAMERAS <<< "${4:-5}"
IFS="," read -r -a NANALYTICS <<< "${5:-3}"
FRAMEWORK="${6:-gst}"
NETWORK="${7:-FP32}"
REGISTRY="$8"
HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

if test -f "${DIR}/docker-compose.yml.m4"; then
    echo "Generating docker-compose.yml"
    m4 -DHOSTIP=${HOSTIP} -DREGISTRY_PREFIX=${REGISTRY} -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DFRAMEWORK=${FRAMEWORK} -DNETWORK_PREFERENCE=${NETWORK} -DNCAMERAS=${NCAMERAS[0]} -DNCAMERAS2=${NCAMERAS[1]:-${NCAMERAS[0]}} -DNCAMERAS3=${NCAMERAS[2]:-${NCAMERAS[1]:-${NCAMERAS[0]}}} -DNANALYTICS=${NANALYTICS[0]} -DNANALYTICS2=${NANALYTICS[1]:-${NANALYTICS[0]}} -DNANALYTICS3=${NANALYTICS[2]:-${NANALYTICS[1]:-${NANALYTICS[0]}}} -DUSER_ID=$(id -u) -DGROUP_ID=$(id -g) -I "${DIR}" "${DIR}/docker-compose.yml.m4" > "${DIR}/docker-compose.yml"
fi
