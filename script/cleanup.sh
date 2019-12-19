#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
YML="${DIR}/../deployment/docker-swarm/docker-compose.yml"
passwd=""
NODEPREFIX="172.32"
for id in $(docker node ls -q 2> /dev/null); do
    ready="$(docker node inspect -f {{.Status.State}} $id)"
    active="$(docker node inspect -f {{.Spec.Availability}} $id)"
    nodeip="$(docker node inspect -f {{.Status.Addr}} $id)"
    labels="$(docker node inspect -f {{.Spec.Labels}} $id | sed 's/map\[/node.labels./' | sed 's/\]$//' | sed 's/ / node.labels./g' | sed 's/:/==/g')"
    role="$(docker node inspect -f {{.Spec.Role}} $id)"

    # skip unavailable or manager node
    if test "$ready" = "ready"; then
        if test "$active" = "active"; then
            if test -z "$(hostname -I | grep --fixed-strings $nodeip)"; then
                if [[ -n $(awk -v labels="$labels node.role=${role}" -f "$DIR/scan-yaml.awk" "$YML") ]]; then

                    if test -n "$(echo $nodeip | grep ${NODEPREFIX})"; then
                        worker="root@$nodeip"
                    else
                        worker="$nodeip"
                    fi

                    echo "Clean up $nodeip..."
                    ssh "$worker" "docker container prune -f"
                    ssh "$worker" "docker volume prune -f"
                    ssh "$worker" "docker network prune -f"
                fi
            fi
        fi
    fi
done

echo "Clean up $(hostname)..."
docker container prune -f
docker volume prune -f
docker network prune -f

