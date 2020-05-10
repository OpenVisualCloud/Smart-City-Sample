#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-traffic}"
NOFFICES="${3:-1}"
IFS="," read -r -a NCAMERAS <<< "${4:-5}"
IFS="," read -r -a NANALYTICS <<< "${5:-3}"
FRAMEWORK="${6:-gst}"
NETWORK="${7:-FP32}"
HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

echo "Generating templates with PLATFORM=${PLATFORM}, SCENARIO=${SCENARIO}, NOFFICES=${NOFFICES}"
find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
    if [[ -n $(grep OFFICE_NAME "$template") ]]; then
        NSCENARIOS=$(echo "include(../../maintenance/db-init/sensor-info.m4)NSCENARIOS" | m4 -I "$DIR")
        for ((SCENARIOIDX=1;SCENARIOIDX<=${NSCENARIOS};SCENARIOIDX++)); do
            for ((OFFICEIDX=1;OFFICEIDX<=${NOFFICES};OFFICEIDX++)); do
                if [[ -n $(echo 'include(office.m4)OFFICE_LOCATION' | m4 -I "$DIR" -DSCENARIO=${SCENARIO} -DSCENARIOIDX=${SCENARIOIDX} -DOFFICEIDX=${OFFICEIDX}) ]]; then
                    yaml=${template/.yaml.m4/-s${SCENARIOIDX}o${OFFICEIDX}.yaml}
                    m4 -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS[0]} -DNCAMERAS2=${NCAMERAS[1]:-${NCAMERAS[0]}} -DNCAMERAS3=${NCAMERAS[2]:-${NCAMERAS[1]:-${NCAMERAS[0]}}} -DNANALYTICS=${NANALYTICS[0]} -DNANALYTICS2=${NANALYTICS[1]:-${NANALYTICS[0]}} -DNANALYTICS3=${NANALYTICS[2]:-${NANALYTICS[1]:-${NANALYTICS[0]}}} -DFRAMEWORK=${FRAMEWORK} -DNETWORK_PREFERENCE=${NETWORK} -DOFFICEIDX=${OFFICEIDX} -DSCENARIOIDX=${SCENARIOIDX} -DUSERID=$(id -u) -DGROUPID=$(id -g) -I "${DIR}" "${template}" > "${yaml}"
                fi
            done
        done
    else
        yaml=${template/.m4/}
        m4 -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS[0]} -DNCAMERAS2=${NCAMERAS[1]:-${NCAMERAS[0]}} -DNCAMERAS3=${NCAMERAS[2]:-${NCAMERAS[1]:-${NCAMERAS[0]}}} -DNANALYTICS=${NANALYTICS[0]} -DNANALYTICS2=${NANALYTICS[1]:-${NANALYTICS[0]}} -DNANALYTICS3=${NANALYTICS[2]:-${NANALYTICS[1]:-${NANALYTICS[0]}}} -DFRAMEWORK=${FRAMEWORK} -DNETWORK_PREFERENCE=${NETWORK} -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} -I "${DIR}" "${template}" > "${yaml}"
    fi
done
