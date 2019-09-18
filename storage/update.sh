#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
REPO=https://raw.githubusercontent.com/OpenVisualCloud/Dockerfiles/master/Xeon/centos-7.6/media/nginx/Dockerfile

NGINX="Dockerfile.1.nginx"
echo "# xeon-centos76-media-nginx" > "$DIR/$NGINX"
wget $REPO -O - >> "$DIR/$NGINX"

