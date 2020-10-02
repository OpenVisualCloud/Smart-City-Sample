#!/bin/bash -e

IMAGE="smtc_api_gateway"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../script/build.sh"
