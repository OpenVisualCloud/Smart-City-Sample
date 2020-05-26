#!/bin/bash -e

function transfer_image {
    image="$1"
    nodeid="$2"
    nodeip="$3"

    # overwrite vcac username
    case "$4" in
    *vcac-zone:yes*|*vcac_zone==yes*)
        worker="root@$nodeip";;
    *)
        worker="$nodeip";;
    esac

    echo "Update image: $image to $worker"
    sig1=$((docker image inspect -f {{.ID}} $image || ((docker pull $image 1>&2) && docker image inspect -f {{.ID}} $image)) | grep .)
    echo " local: $sig1"

    hostfile="$HOME/.vcac-hosts"
    if [ ! -f "$hostfile" ]; then hostfile="/etc/vcac-hosts"; fi
    host=$(awk -v node="$nodeid/$nodeip" '$1==node{print$2}' "$hostfile" 2>/dev/null || true)
    if [ -z "$host" ]; then host=$(hostname); fi

    CONNECTION_TIMEOUT=1
    case "$(hostname -f)" in
        $host | $host.*) # direct access
            sig2=$(ssh -o ConnectTimeout=$CONNECTION_TIMEOUT $worker "docker image inspect -f {{.ID}} $image 2> /dev/null || echo" || true)
            echo "remote: $sig2"

            if test "$sig1" != "$sig2"; then
                echo "Transfering image..."
                (docker save $image | ssh -o ConnectTimeout=$CONNECTION_TIMEOUT $worker "docker image rm -f $image 2>/dev/null; docker load") || true
            fi;;
        *) # access via jump host
            sig2=$(ssh -o ConnectTimeout=$CONNECTION_TIMEOUT $host "ssh -o ConnectTimeout=$CONNECTION_TIMEOUT $worker \"docker image inspect -f {{.ID}} $image 2> /dev/null || echo\"" || true)
            echo "remote: $sig2"

            if test "$sig1" != "$sig2"; then
                echo "Transfering image..."
                (docker save $image | ssh -o ConnectTimeout=$CONNECTION_TIMEOUT $host "ssh -o ConnectTimeout=$CONNECTION_TIMEOUT $worker \"docker image rm -f $image 2>/dev/null; docker load\"") || true
            fi;;
    esac
    echo ""
}

DIR=$(dirname $(readlink -f "$0"))
docker node ls > /dev/null 2> /dev/null && (
    echo "Updating docker-swarm nodes..."
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
                    for image in $(awk -v labels="$labels node.role=${role}" -f "$DIR/scan-yaml.awk" "${DIR}/../deployment/docker-swarm/docker-compose.yml"); do
                        transfer_image $image "$id" "$nodeip" "$labels"
                    done
                fi
            fi
        fi
    done
) || echo -n ""

kubectl get node >/dev/null 2>/dev/null && (
    echo "Updating Kubernetes nodes..."
    for id in $(kubectl get nodes --selector='!node-role.kubernetes.io/master' 2> /dev/null | grep ' Ready ' | cut -f1 -d' '); do
        nodeip="$(kubectl describe node $id | grep InternalIP | sed -E 's/[^0-9]+([0-9.]+)$/\1/')"
        labels="$(kubectl describe node $id | awk '/Annotations:/{lf=0}/Labels:/{sub("Labels:","",$0);lf=1}lf==1{sub("=",":",$1);print$1}')"

        for image in $(awk -v labels="$labels" -f "$DIR/scan-yaml.awk" "${DIR}/../deployment/kubernetes/yaml"/*.yaml); do
            transfer_image $image "$id" "$nodeip" "$labels"
        done
    done
) || echo -n ""
