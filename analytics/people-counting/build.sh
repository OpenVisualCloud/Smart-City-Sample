#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-traffic}"

case "$SCENARIO" in
    *stadium*)
        . "$DIR/../../script/build.sh"
        ;;
esac
