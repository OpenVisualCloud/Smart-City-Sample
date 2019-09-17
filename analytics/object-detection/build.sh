#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
SCENARIO="${2:-traffic}"

case "$SCENARIO" in
    *traffic*)
        cp -f "$DIR/../../script/db_query.py" "$DIR/../../script/db_ingest.py" "$DIR/../../script"/dsl_*.py "$DIR"
        . "$DIR/../../script/build.sh"
        ;;
esac
