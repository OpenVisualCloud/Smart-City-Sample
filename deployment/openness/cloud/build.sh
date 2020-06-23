#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-traffic}"
NOFFICES="${3:-1}"
IFS="," read -r -a NCAMERAS <<< "${4:-5}"
IFS="," read -r -a NANALYTICS <<< "${5:-3}"
FRAMEWORK="${6:-gst}"
REGISTRY="$8"
HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

echo "Generating templates with PLATFORM=${PLATFORM}, SCENARIO=${SCENARIO}, NOFFICES=${NOFFICES}"
find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
    m4 -DREGISTRY=${REGISTRY} -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS[0]} -DNCAMERAS2=${NCAMERAS[1]:-${NCAMERAS[0]}} -DNANALYTICS=${NANALYTICS[0]} -DNANALYTICS2=${NANALYTICS[1]:-${NANALYTICS[0]}} -DFRAMEWORK=${FRAMEWORK} -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} -I "${DIR}" "${template}" > "${template/.m4/}"
done
