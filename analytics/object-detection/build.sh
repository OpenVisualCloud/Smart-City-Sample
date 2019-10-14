#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-traffic}"
FRAMEWORK="${6:-gst}"

case "$SCENARIO" in
    *traffic*)
        . "$DIR/../../script/build.sh"
        ;;
esac
