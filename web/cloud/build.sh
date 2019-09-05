#!/bin/bash -e

IMAGE="smtc_web_cloud"
DIR=$(dirname $(readlink -f "$0"))
SCENARIO="${2:-traffic}"

cp -f "$DIR/../../script/db_query.py" "$DIR/../../script/"/dsl_*.py "$DIR"
echo "settings.scenarios=[\"$SCENARIO\"];" > "$DIR/html/js/scenario.js"
. "$DIR/../../script/build.sh"
