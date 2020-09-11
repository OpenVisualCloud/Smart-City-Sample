#!/bin/bash -e

IMAGE="smtc_db_init"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/mkm4.sh"
. "$DIR/../../script/build.sh"
