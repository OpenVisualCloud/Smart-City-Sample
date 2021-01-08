#!/bin/bash -e

IMAGE="smtc_rtmp_discovery"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
