#!/bin/bash -e

IMAGE="smtc_ssl_tunnel"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"

