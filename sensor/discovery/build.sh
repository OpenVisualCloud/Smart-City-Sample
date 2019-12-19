#!/bin/bash -e

IMAGE="smtc_onvif_discovery"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
