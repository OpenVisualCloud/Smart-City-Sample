#!/bin/bash -e

# Build VA Service from Github 
AD_INSERTION_REPO="https://github.com/OpenVisualCloud/Ad-Insertion-Sample.git"
VA_FOLDER="ad-insertion/video-analytics-service"
USER="docker"
GROUP="docker"
AD_INSERTION_TAG="v1.1"

typeset -l platform

PLATFORM=Xeon
platform=${PLATFORM}

sudo docker build ${AD_INSERTION_REPO}\#${AD_INSERTION_TAG}:${VA_FOLDER} --file platforms/${PLATFORM}/Dockerfile.2.gst.${platform} --target build -t "${platform}-ubuntu1804-dldt-gst-va:build" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)

sudo docker build ${AD_INSERTION_REPO}\#${AD_INSERTION_TAG}:${VA_FOLDER} --file platforms/${PLATFORM}/Dockerfile.2.gst.${platform} -t "${platform}-ubuntu1804-dldt-gst-va:latest" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)

sudo docker build ${AD_INSERTION_REPO}\#${AD_INSERTION_TAG}:${VA_FOLDER} --file platforms/${PLATFORM}/Dockerfile.1.va.gst.${platform} -t "video_analytics_service_gstreamer:latest" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)

#IMAGE="smtc_analytics_recording"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script/db_query.py" "$DIR/../../script/db_ingest.py" "$DIR/../../script"/dsl_*.py "$DIR/../../script/probe.py" "$DIR"
. "$DIR/../../script/build.sh"

# build image(s) in order (to satisfy dependencies)
for dep in '.8.*' '.7.*' '.6.*' '.5.*' '.4.*' '.3.*' '.2.*' '.1.*' '.0.*' ''; do
    for dockerfile in `find "${DIR}/platforms/${PLATFORM}" -maxdepth 1 -name "Dockerfile${dep}" -print`; do
        image=$(head -n 1 "$dockerfile" | grep '# ' | cut -d' ' -f2)
        if test -z "$image"; then image="$IMAGE"; fi

        if grep -q 'AS build' "$dockerfile"; then
            echo sudo docker build --file="$dockerfile" --target build -t "$image:build" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)
            sudo docker build --file="$dockerfile" --target build -t "$image:build" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)
        fi

        echo sudo docker build --file="$dockerfile" -t "$image:latest" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)
        sudo docker build --file="$dockerfile" -t "$image:latest" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)
    done
done

