#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-traffic}"
NOFFICES="${3:-1}"
NCAMERAS="${4:-5}"
NANALYTICS="${5:-3}"

echo "Generating templates with PLATFORM=${PLATFORM}, SCENARIO=${SCENARIO}, NOFFICES=${NOFFICES}"
find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
    if [[ -n $(grep OFFICE_NAME "$template") ]]; then
        NSCENARIOS=$(echo "include(../../script/scenario.m4)NSCENARIOS" | m4 -I "$DIR")
        for ((SCENARIOIDX=1;SCENARIOIDX<=${NSCENARIOS};SCENARIOIDX++)); do
            for ((OFFICEIDX=1;OFFICEIDX<=${NOFFICES};OFFICEIDX++)); do
                if [[ -n $(echo 'include(office.m4)OFFICE_LOCATION' | m4 -I "$DIR" -DSCENARIO=${SCENARIO} -DSCENARIOIDX=${SCENARIOIDX} -DOFFICEIDX=${OFFICEIDX}) ]]; then
                    yaml=${template/.yaml.m4/-s${SCENARIOIDX}o${OFFICEIDX}.yaml}
                    m4 -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS} -DNANALYTICS=${NANALYTICS} -DOFFICEIDX=${OFFICEIDX} -DSCENARIOIDX=${SCENARIOIDX} -DUSERID=$(id -u) -DGROUPID=$(id -g) -I "${DIR}" "${template}" > "${yaml}"
                fi
            done
        done
    else
        yaml=${template/.m4/}
        m4 -DNOFFICES=${NOFFICES} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DNCAMERAS=${NCAMERAS} -DNANALYTICS=${NANALYTICS} -DUSERID=$(id -u) -DGROUPID=$(id -g) -I "${DIR}" "${template}" > "${yaml}"
    fi
done
