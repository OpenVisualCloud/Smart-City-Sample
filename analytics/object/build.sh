#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

. "$DIR/download-models.sh" # download model

. "$DIR/../../script/build.sh"
