#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
SCENARIO="${2:-stadium}"
FRAMEWORK="${6:-gst}"

case "$FRAMEWORK" in
    gst)
        ;;
    *)
        echo "Not Implemented"
        exit -1
        ;;
esac 

case "$SCENARIO" in
    *stadium*)
        . "$DIR/../../script/build.sh"
        ;;
esac
