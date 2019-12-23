#!/bin/sh

function gracefully_exit {
    docker kill $(docker ps --format {{.ID}} --filter name=$HOSTNAME)
    exit 0
}

trap gracefully_exit SIGTERM

# setting
ENVS="$(env | grep ^VCAC_ | sed 's/^VCAC_/-e /')"
NETWORKS="$(docker inspect $HOSTNAME --format {{.NetworkSettings.Networks}} | sed -e 's/^map\[\(.*\)]/\1/' -e 's/\(.*\):.*/--network \1/')"
BINDS="$(docker inspect $HOSTNAME --format {{.HostConfig.Mounts}} | sed -e 's/ \+/:/g' -e 's/:<nil>//g' -e 's/}:{/ /g' -e 's/\[{//' -e 's/}]//' -e 's/bind:/-v /g' -e 's/:true/:ro/g' -e 's/:false/:rw/g')"

# docker run
/usr/local/bin/docker-entrypoint.sh docker run --rm --name $HOSTNAME --user root -v /tmp:/tmp -v /var/tmp:/var/tmp --device=/dev/ion:/dev/ion --privileged $ENVS $NETWORKS $BINDS "$@" $VCAC_IMAGE &

wait
