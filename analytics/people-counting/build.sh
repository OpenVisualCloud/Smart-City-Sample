#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-stadium}"
FRAMEWORK="${6:-gst}"

case "$SCENARIO" in
    *stadium*)
        . "$DIR/../../script/build.sh"
        ;;
esac
