#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
SCENARIO="${2:-traffic}"

case "$SCENARIO" in
    *traffic*)
        . "$DIR/../../script/build.sh"
        ;;
esac
