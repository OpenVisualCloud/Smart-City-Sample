#!/bin/bash -e

DOCKER_REPO=${DOCKER_REPO="https://raw.githubusercontent.com/OpenVisualCloud/Dockerfiles/v1.0/Xeon/centos-7.6"}

DIR=$(dirname $(readlink -f "$0"))

(echo "# xeon-centos76-ffmpeg"; curl ${DOCKER_REPO}/ffmpeg/Dockerfile) > "$DIR/Dockerfile.1.ffmpeg"
