#!/bin/sh

function gracefully_exit {
    docker kill $(docker ps --format {{.ID}} --filter name=$HOSTNAME)
    exit 0
}

trap gracefully_exit SIGTERM

# network setting
NETWORK=$(docker inspect $HOSTNAME --format {{.NetworkSettings.Networks}} | sed -e 's/^map\[\(.*\)]/\1/' -e 's/\(.*\):.*/--network \1/')
BINDS="$(docker inspect $HOSTNAME --format {{.HostConfig.Mounts}} | sed -e 's/ \+/:/g' -e 's/:<nil>//g' -e 's/}:{/ /g' -e 's/\[{//' -e 's/}]//' -e 's/bind:/-v /g' -e 's/:true/:ro/g' -e 's/:false/:rw/g')"

# docker run
echo /usr/local/bin/docker-entrypoint.sh docker run $(env | grep ^VCAC_ | sed -e 's/^VCAC_\(.*\)=.*/-e \1/') --rm --name $HOSTNAME --user root -v /tmp:/tmp -v /var/tmp:/var/tmp --device=/dev/ion:/dev/ion --privileged $NETWORK $BINDS "$@" $VCAC_IMAGE
/usr/local/bin/docker-entrypoint.sh docker run $(env | grep ^VCAC_ | sed -e 's/^VCAC_\(.*\)=.*/-e \1/') --rm --name $HOSTNAME --user root -v /tmp:/tmp -v /var/tmp:/var/tmp --device=/dev/ion:/dev/ion --privileged $NETWORK $BINDS "$@" $VCAC_IMAGE &

wait
