#!/bin/bash -e

IMAGE="smtc_trigger_health"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script/db_query.py" "$DIR/../../script/db_ingest.py" "$DIR/../../script"/dsl_*.py "$DIR"
. "$DIR/../../script/build.sh"
