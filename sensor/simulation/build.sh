#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
IMAGE="smtc_sensor_simulation"

. "$DIR/download.sh" # download content
. "$DIR/../../script/build.sh"
