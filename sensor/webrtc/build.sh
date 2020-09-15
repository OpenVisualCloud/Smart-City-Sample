#!/bin/bash -e

IMAGE="smtc_sensor_webrtc"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
