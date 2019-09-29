#!/bin/bash -e

IMAGE="smtc_where_indexing"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
