#!/bin/bash -e

IMAGE="smtc_trigger_health"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
