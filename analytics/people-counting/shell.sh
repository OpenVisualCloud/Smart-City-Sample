#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
IMAGE="smtc_analytics_people_counting_$(echo ${PLATFORM} | tr A-Z a-z)"

. "$DIR/../../script/shell.sh"
