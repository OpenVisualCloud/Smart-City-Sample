#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
shift
FRAMEWORK="${1:-gst}"
shift

IMAGE="smtc_analytics_people_counting_$(echo ${PLATFORM} | tr A-Z a-z)_$(echo ${FRAMEWORK} | tr A-Z a-z)"
. "$DIR/../../script/shell.sh"
