#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
XEON_DIR=$DIR/platforms/Xeon
VCAC_A_DIR=$DIR/platforms/VCAC-A
AD_INSERT_TAG=v1.1
DOCKERFILE_TAG=master

# ffmpeg base image on centos
DOCKER_REPO=${DOCKER_REPO="https://raw.githubusercontent.com/OpenVisualCloud/Dockerfiles/v1.0/Xeon/centos-7.6"}

base_name=xeon-centos76-ffmpeg
docker_file="$XEON_DIR/Dockerfile.1.ffmpeg"

echo "# xeon-centos76-ffmpeg" > ${docker_file}
curl ${DOCKER_REPO}/ffmpeg/Dockerfile >> ${docker_file} 

###################################################################################################################

# gst va service base dockerfile
DOCKER_REPO="https://raw.githubusercontent.com/OpenVisualCloud/Ad-Insertion-Sample/${AD_INSERT_TAG}/ad-insertion/video-analytics-service/platforms/Xeon/Dockerfile.1.va.gst.xeon"
docker_file="$XEON_DIR/Dockerfile.11.gst.va.xeon"
curl ${DOCKER_REPO} > ${docker_file}

# gst base dockerfile
DOCKER_REPO="https://raw.githubusercontent.com/OpenVisualCloud/Ad-Insertion-Sample/${AD_INSERT_TAG}/ad-insertion/video-analytics-service/platforms/Xeon/Dockerfile.2.gst.xeon"
docker_file="$XEON_DIR/Dockerfile.12.gst.xeon"
curl ${DOCKER_REPO} > ${docker_file}
