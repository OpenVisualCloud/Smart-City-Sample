#!/bin/bash -e

if test -z "${DIR}"; then
    echo "This script should not be called directly."
    exit -1
fi

pid="$(sudo docker ps -f ancestor=$IMAGE --format='{{.ID}}' | head -n 1)"
if [ -n "$pid" ] && [ "$#" -le "1" ]; then
    echo "bash into running container...$IMAGE"
    sudo docker exec -it $pid ${*-/bin/bash}
else
    echo "bash into new container...$IMAGE"
    if test -z "$DOCKERFILE"; then
        DOCKERFILE="${DIR}/Dockerfile"
    fi
    args=("$@")
    sudo docker run ${OPTIONS[@]} $(env | grep -E '_(proxy)=' | sed 's/^/-e /') $(grep '^ARG .*=' "$DOCKERFILE" | sed 's/^ARG /-e /') --entrypoint ${1:-/bin/bash} -it "${IMAGE}" ${args[@]:1}
fi

