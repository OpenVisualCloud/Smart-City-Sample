#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-stadium}"

case "$SCENARIO" in
    *stadium*)
        . "$DIR/../../script/build.sh"
        ;;
esac
