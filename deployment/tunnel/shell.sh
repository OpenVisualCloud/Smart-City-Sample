#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
IMAGE="smtc_ssh_tunnel"
OPTIONS=(-v "$DIR:/home:rw")

. "$DIR/../../script/shell.sh"
