#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
IMAGE="smtc_sensor_simulation"

. "$DIR/download.sh" # download content
cp -f "$DIR/../../script/db_ingest.py" "$DIR/../../script/probe.py" "$DIR"
. "$DIR/../../script/build.sh"
