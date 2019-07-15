#!/bin/bash -e

IMAGE="smtc_sensor_simulation"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script/db_ingest.py" "$DIR"
. "$DIR/../../script/build.sh"
