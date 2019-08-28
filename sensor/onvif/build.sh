#!/bin/bash -e

IMAGE="smtc_onvif_discovery"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script/db_query.py" "$DIR/../../script/db_ingest.py" "$DIR/../../script"/dsl_*.py "$DIR/../../script/probe.py" "$DIR"
. "$DIR/../../script/build.sh"
