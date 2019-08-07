#!/bin/bash -e

# Build VA Service from Github 
AD_INSERTION_REPO="https://github.com/OpenVisualCloud/Ad-Insertion-Sample.git"
VA_FOLDER="ad-insertion/video-analytics-service"
USER="docker"
GROUP="docker"

sudo docker build ${AD_INSERTION_REPO}\#v1.1:${VA_FOLDER} --file platforms/Xeon/Dockerfile.2.gst.xeon -t "xeon-ubuntu1804-dldt-gst-va:latest" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)

sudo docker build ${AD_INSERTION_REPO}\#v1.1:${VA_FOLDER} --file platforms/Xeon/Dockerfile.1.va.gst.xeon -t "smtc_analytics_common:latest" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)

