#!/bin/bash -e

IMAGE="smtc_onvif_discovery"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script"/dsl_*.py "$DIR/../../script"/db_*.py "$DIR"
. "$DIR/../../script/build.sh"
