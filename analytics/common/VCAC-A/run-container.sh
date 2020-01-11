#!/bin/sh

function gracefully_exit {
    docker kill $(docker ps --format {{.ID}} --filter name=$HOSTNAME)
    exit 0
}

# gracefully exit
trap gracefully_exit SIGTERM

# setting
ENVS="$(env | grep ^VCAC_ | sed 's/^VCAC_/-e /')"
NETWORKS="$(docker inspect $HOSTNAME --format {{.NetworkSettings.Networks}} | sed -e 's/map\[\(.*\)]/\1/' -e 's/\([A-Za-z0-9_]*\):[^ ]*/--network=\1/g')"
BINDS="$(docker inspect $HOSTNAME --format {{.HostConfig.Mounts}} | sed -e 's/\[\(.*\)]/\1/' -e 's/{\([a-z]*\) \([^ ]*\) \([^ ]*\) \([a-z]*\)[^}]*}/-v \2:\3:\4/g' -e 's/:true/:ro/g' -e 's/:false/:rw/g')"

# docker run
/usr/local/bin/docker-entrypoint.sh docker run --rm --name $HOSTNAME --user root -v /var/tmp:/var/tmp --privileged $ENVS $NETWORKS $BINDS "$@" $VCAC_IMAGE &

wait
