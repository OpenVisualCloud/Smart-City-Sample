#!/bin/bash -e

function transfer_image {
    image="$1"
    nodeip="$2"

    # overwrite vcac username
    case "$3" in
    *vcac-zone:yes*|*vcac_zone==yes*)
        worker="root@$nodeip";;
    *)
        worker="$nodeip";;
    esac

    echo "Update image: $image to $worker"
    sig1=$((docker image inspect -f {{.ID}} $image || ((docker pull $image 1>&2) && docker image inspect -f {{.ID}} $image)) | grep .)
    echo " local: $sig1"

    CONNECTION_TIMEOUT=1
    sig2=$(ssh -o ConnectTimeout=$CONNECTION_TIMEOUT $worker "docker image inspect -f {{.ID}} $image 2> /dev/null || echo" || true)
    echo "remote: $sig2"

    if test "$sig1" != "$sig2"; then
        echo "Transfering image..."
        (docker save $image | ssh -o ConnectTimeout=$CONNECTION_TIMEOUT $worker "docker image rm -f $image 2>/dev/null; docker load") || true
    fi
    echo ""
}

DIR=$(dirname $(readlink -f "$0"))
YML="${DIR}/../deployment/docker-swarm/docker-compose.yml"
for id in $(docker node ls -q 2> /dev/null); do
    ready="$(docker node inspect -f {{.Status.State}} $id)"
    active="$(docker node inspect -f {{.Spec.Availability}} $id)"
    nodeip="$(docker node inspect -f {{.Status.Addr}} $id)"
    labels="$(docker node inspect -f {{.Spec.Labels}} $id | sed 's/map\[/node.labels./' | sed 's/\]$//' | sed 's/ / node.labels./g' | sed 's/:/==/g')"
    role="$(docker node inspect -f {{.Spec.Role}} $id)"

    if test "$ready" = "ready"; then
        if test "$active" = "active"; then
            # skip unavailable or manager node
            if test -z "$(hostname -I | grep --fixed-strings $nodeip)"; then
                for image in $(awk -v labels="$labels node.role=${role}" -f "$DIR/scan-yaml.awk" "$YML"); do
                    transfer_image $image "$nodeip" "$labels"
                done
            fi
        fi
    fi
done

if [ -x /usr/bin/kubectl ] || [ -x /usr/local/bin/kubectl ]; then
    for id in $(kubectl get nodes --selector='!node-role.kubernetes.io/master' 2> /dev/null | grep ' Ready ' | cut -f1 -d' '); do
        nodeip="$(kubectl describe node $id | grep InternalIP | sed -E 's/[^0-9]+([0-9.]+)$/\1/')"
        labels="$(kubectl describe node $id | awk '/Annotations:/{lf=0}/Labels:/{sub("Labels:","",$0);lf=1}lf==1{sub("=",":",$1);print$1}')"

        for image in $(awk -v labels="$labels" -f "$DIR/scan-yaml.awk" "${DIR}/../deployment/kubernetes"/*.yaml); do
            transfer_image $image "$nodeip" "$labels"
        done
    done
fi
