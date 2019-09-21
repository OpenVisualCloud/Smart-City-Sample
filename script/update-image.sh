#!/bin/bash -e

function transfer_image {
    image="$1"
    worker="$2"

    echo "Update image: $image to $worker"
    sig1=$(docker image inspect -f {{.ID}} $image)
    echo " local: $sig1"

    sig2=$(ssh $worker "docker image inspect -f {{.ID}} $image 2> /dev/null || echo")
    echo "remote: $sig2"

    if test "$sig1" != "$sig2"; then
        echo "Transfering image..."
        docker save $image | ssh $worker "docker image rm -f $image 2>/dev/null; docker load"
    fi
    echo ""
}

DIR=$(dirname $(readlink -f "$0"))
YML="${DIR}/../deployment/docker-swarm/docker-compose.yml"
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

                for image in $(awk -v constraints=1 -v role="node.role==${role}" -v labels="$labels" -f "$DIR/scan-yml.awk" "$YML"); do

                    # trasnfer VCAC-A images to VCAC-A nodes only
                    if [[ -n "$(echo $nodeip | grep --fixed-strings 172.32.1.1)" ]] || [[ "$(id -u)" -eq "0" ]]; then
                        transfer_image $image "root@$nodeip"
                    else
                        transfer_image $image "$nodeip"
                    fi

                done

            fi
        fi
    fi
done
