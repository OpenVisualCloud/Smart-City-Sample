#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-traffic}"
NOFFICES="${3:-1}"
NCAMERAS="${4:-5}"
NANALYTICS="${5:-3}"

for template in "${DIR}/*.m4"; do
    echo "Generating ${template/.mp4/} with PLATFORM=${PLATFORM}, SCENARIO=${SCENARIO}, NOFFICES=${NOFFICES}"
    m4 -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS} -DNANALYTICS=${NANALYTICS} -I "${DIR}" "${DIR}/${template}" > "${DIR}/${template/.mp4/}"
done
