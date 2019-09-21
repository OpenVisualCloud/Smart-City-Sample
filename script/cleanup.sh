#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
YML="${DIR}/../deployment/docker-swarm/docker-compose.yml"
passwd=""
for id in $(docker node ls -q 2> /dev/null); do
    ready="$(docker node inspect -f {{.Status.State}} $id)"
    active="$(docker node inspect -f {{.Spec.Availability}} $id)"
    nodeip="$(docker node inspect -f {{.Status.Addr}} $id)"
    labels="$(docker node inspect -f {{.Spec.Labels}} $id)"
    role="$(docker node inspect -f {{.Spec.Role}} $id)"

    # skip unavailable or manager node
    if test "$ready" = "ready"; then
        if test "$active" = "active"; then
            if test -z "$(hostname -I | grep --fixed-strings $nodeip)"; then
                if [[ -n $(awk -v constraints=1 -v role="node.role==${role}" -v labels="$labels" -f "$DIR/scan-yml.awk" "$YML") ]]; then

                    if test -n "$(echo $nodeip | grep --fixed-strings 172.32.1.1)"; then
                        worker="root@$nodeip"
                    else
                        worker="$nodeip"
                    fi

                    #ssh "$worker" "docker container prune -f"
                    ssh "$worker" "docker volume prune -f"
                    #ssh "$worker" "docker network prune -f"
                fi
            fi
        fi
    fi
done

#docker container prune -f
docker volume prune -f
#docker network prune -f

