#!/bin/bash -e

IMAGE="smtc_ssl_tunnel"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=(-v "$DIR:/home:rw")

. "$DIR/../../script/shell.sh"

