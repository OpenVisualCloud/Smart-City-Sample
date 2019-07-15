#!/bin/bash -e

IMAGE="smtc_trigger_health"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script/"db_*.py "$DIR/../../script"/dsl_*.py "$DIR"
. "$DIR/../../script/build.sh"
