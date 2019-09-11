#!/bin/sh

function gracefully_exit {
    PGID=$(ps -o pgid= $$ | grep -o [0-9]*)
    setsid kill -- -$PGID
    exit 0
}

trap gracefully_exit SIGTERM

case "$1" in
    -*)
        # docker run commands and arguments
        exec /usr/local/bin/docker-entrypoint.sh docker run $(env | grep ^VCAC_ | sed 's/^VCAC_/-e /') --user root -v /tmp:/tmp -v /var/tmp:/var/tmp -v /etc/localtime:/etc/localtime:ro --device=/dev/ion:/dev/ion --privileged "$@" &
        ;;
    *)
        # regular commands
        exec /usr/local/bin/docker-entrypoint.sh "$@" &
        ;;
esac

wait
