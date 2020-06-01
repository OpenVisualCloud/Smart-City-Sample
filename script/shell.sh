#!/bin/bash -e

if test -z "${DIR}"; then
    echo "This script should not be called directly."
    exit -1
fi

pid="$(docker ps -f ancestor=$IMAGE --format='{{.ID}}' | head -n 1)"
if [ -n "$pid" ] && [ "$#" -eq 0 ]; then
    echo "bash into running container...$IMAGE"
    docker exec -it $pid ${*-/bin/bash}
else
    echo "bash into new container...$IMAGE"
    args=("$@")
    docker run --rm ${OPTIONS[@]} $(env | cut -f1 -d= | grep -E '_(proxy|REPO|VER)$' | sed 's/^/-e /') --entrypoint ${1:-/bin/bash} -it "${IMAGE}" ${args[@]:1}
fi
