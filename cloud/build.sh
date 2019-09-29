#!/bin/bash -e

IMAGE="smtc_web_cloud"
DIR=$(dirname $(readlink -f "$0"))
SCENARIO="${2:-traffic}"

echo "settings.scenarios=\"$SCENARIO\".split(',');" > "$DIR/html/js/scenario.js"
. "$DIR/../script/build.sh"
