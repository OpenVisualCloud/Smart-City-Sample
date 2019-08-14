#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"

echo "Build platform $PLATFORM..."
. "${DIR}/../../script/build.sh"
