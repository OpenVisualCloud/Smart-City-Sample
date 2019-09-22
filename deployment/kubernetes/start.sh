#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="${4:-1}"
yml="$DIR/docker-compose.yml"


export USER_ID="$(id -u)"
export GROUP_ID="$(id -g)"
echo "Cleanup..."
$DIR/../../script/cleanup.sh; echo

"$DIR/../certificate/self-sign.sh"
shift
. "$DIR/build.sh"
kubectl apply -f "$yml"
