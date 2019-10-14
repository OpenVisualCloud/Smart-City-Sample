#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
FRAMEWORK="${6:-gst}"
IMAGE="smtc_analytics_object_detection_$(echo ${PLATFORM} | tr A-Z a-z)_$(echo ${FRAMEWORK} | tr A-Z a-z)"

. "$DIR/../../script/shell.sh"
