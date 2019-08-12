#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="$1"

cp -f "$DIR/../../script/db_query.py" "$DIR/../../script/db_ingest.py" "$DIR/../../script"/dsl_*.py "$DIR/../../script/probe.py" "$DIR"
. "$DIR/../../script/build.sh"
