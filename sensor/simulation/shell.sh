#!/bin/bash -e

IMAGE="smtc_sensor_simulation"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=("--volume=$DIR/../../volume/simulated:/mnt/simulated:ro")

. "$DIR/../../script/shell.sh"
