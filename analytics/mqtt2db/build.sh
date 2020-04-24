#!/bin/bash -e

IMAGE="smtc_mqtt2db"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
