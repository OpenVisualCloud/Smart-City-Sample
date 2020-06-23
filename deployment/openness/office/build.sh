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
IFS=',' read -a camera_host_array <<< $CAMERA_HOSTS
if [ ${#camera_host_array[@]} -ne ${NOFFICES} ];then
  echo "The number of camera hosts shall be the same number of offices!"
  exit 0
fi

echo "Generating templates with PLATFORM=${PLATFORM}, SCENARIO=${SCENARIO}, NOFFICES=${NOFFICES}"
find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
    m4 -DREGISTRY_PREFIX=${REGISTRY} -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS[0]} -DNCAMERAS2=${NCAMERAS[1]:-${NCAMERAS[0]}} -DNANALYTICS=${NANALYTICS[0]} -DNANALYTICS2=${NANALYTICS[1]:-${NANALYTICS[0]}} -DFRAMEWORK=${FRAMEWORK} -DNETWORK_PREFERENCE=${NETWORK} -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} -DCAMERA_HOST=${CAMERA_HOST} -DCLOUD_HOST=${CLOUD_HOST} -I "${DIR}" "${template}" > "${template/.m4/}"
done
