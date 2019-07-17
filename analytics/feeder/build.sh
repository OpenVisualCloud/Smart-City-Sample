#!/bin/bash -e

# Build VA Service from Github 
AD_INSERTION_REPO="https://github.com/OpenVisualCloud/Ad-Insertion-Sample.git"
VA_FOLDER="ad-insertion/video-analytics-service"
USER="docker"
GROUP="docker"

sudo docker build ${AD_INSERTION_REPO}\#master:${VA_FOLDER} --file platforms/Xeon/Dockerfile.2.gst.xeon --target build -t "xeon-ubuntu1804-dldt-gst-va:build" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)

sudo docker build ${AD_INSERTION_REPO}\#master:${VA_FOLDER} --file platforms/Xeon/Dockerfile.2.gst.xeon -t "xeon-ubuntu1804-dldt-gst-va:latest" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)

sudo docker build ${AD_INSERTION_REPO}\#master:${VA_FOLDER} --file platforms/Xeon/Dockerfile.1.va.gst.xeon -t "video_analytics_service_gstreamer:latest" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)

#IMAGE="smtc_analytics_recording"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script/db_query.py" "$DIR/../../script/db_ingest.py" "$DIR/../../script"/dsl_*.py "$DIR/../../script/probe.py" "$DIR"
. "$DIR/../../script/build.sh"
