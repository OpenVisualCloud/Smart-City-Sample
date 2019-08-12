#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="$1"

echo "Build platform $PLATFORM..."
. "${DIR}/../../script/build.sh"
