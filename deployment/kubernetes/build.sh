#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-traffic}"
NOFFICES="${3:-1}"
NCAMERAS="${4:-5}"
NANALYTICS="${5:-3}"

echo "Generating templates with PLATFORM=${PLATFORM}, SCENARIO=${SCENARIO}, NOFFICES=${NOFFICES}"
find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
master=$(kubectl get nodes  | grep master | cut -f1 -d' ')
for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
    case $(head -n 1 "$template") in
    *OFFICEIDX*)
        for ((OFFICEIDX=1;OFFICEIDX<=${NOFFICES};OFFICEIDX++)); do
            yaml=${template/.yaml.m4/-office${OFFICEIDX}.yaml}
            m4 -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS} -DNANALYTICS=${NANALYTICS} -DOFFICEIDX=${OFFICEIDX} -DHOSTNAME=${master} -I "${DIR}" "${template}" > "${yaml}"
        done;;
    *)
        yaml=${template/.m4/}
        m4 -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS} -DNANALYTICS=${NANALYTICS} -DHOSTNAME=${master} -I "${DIR}" "${template}" > "${yaml}";;
    esac
done
