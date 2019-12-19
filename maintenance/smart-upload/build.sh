#!/bin/bash -e

IMAGE="smtc_smart_upload"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
