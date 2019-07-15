#!/bin/bash -e

IMAGE="smtc_certificate"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
