#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
IMAGE="smtc_ssh_tunnel"

. "$DIR/../../script/build.sh"

