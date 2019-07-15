#!/bin/bash -e

IMAGE="smtc_storage_cleanup"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/shell.sh"
