#!/bin/bash -e

IMAGE="smtc_onvif_discovery"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=(-e PORT_SCAN)

. "$DIR/../../script/shell.sh"
