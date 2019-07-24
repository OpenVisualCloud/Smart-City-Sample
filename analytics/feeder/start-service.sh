#!/bin/bash -e

cd /home/video-analytics/app/server
python3 -m openapi_server $@ &
pid1="${!}"

cd /home
./main.py &
pid2="${!}"

quit_nicely() {
    kill -SIGTERM "$pid1" "$pid2"
    wait "$pid1" "$pid2"
    exit 143
}

trap 'kill ${!}; quit_nicely' SIGTERM

while true; do
    tail -f /dev/null & wait "$pid1" "$pid2"
done
