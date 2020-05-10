#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="$(echo ${2:-traffic} | tr ',' '/')"
NOFFICES="${3:-1}"
NCAMERAS="$(echo ${4:-5} | tr ',' '/')"
NANALYTICS="$(echo ${5:-3} | tr ',' '/')"
FRAMEWORK="${6:-gst}"
NETWORK="$(echo ${7:-FP32} | tr ',' '/')"
HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

echo "Generating helm chart with PLATFORM=${PLATFORM}, SCENARIO=${SCENARIO}, NOFFICES=${NOFFICES}"
m4 -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS} -DNANALYTICS=${NANALYTICS} -DFRAMEWORK=${FRAMEWORK} -DNETWORK_PREFERENCE=${NETWORK} -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} -I "${DIR}/smtc" "$DIR/smtc/values.yaml.m4" > "$DIR/smtc/values.yaml"
