#!/bin/bash -e

function transfer_image {
    image="$1"
    worker="$2"
    passwd="$3"

    echo "Update image: $image to $worker"
    sig1=$(sudo docker image inspect -f {{.ID}} $image)
    echo " local: $sig1"

    case "$worker" in
        root@*)
            sig2=$(ssh $worker "docker image inspect -f {{.ID}} $image 2> /dev/null || echo");;
        *)
            sig2=$(echo $passwd | ssh $worker cat \| sudo --prompt="" -S -- "docker image inspect -f {{.ID}} $image 2> /dev/null || echo");;
    esac
    echo "remote: $sig2"

    if test "$sig1" != "$sig2"; then
        case "$worker" in
            root@*)
                sudo docker save $image | ssh $worker "docker image rm -f $image 2>/dev/null; docker load";;
            *)
                ( echo $passwd ; sudo docker save $image ) | ssh $worker cat \| sudo --prompt="" -S -- "docker load"
        esac
    fi
    echo ""
}

DIR=$(dirname $(readlink -f "$0"))
YML="${DIR}/../deployment/docker-swarm/docker-compose.yml"
passwd=""
for id in $(sudo docker node ls -q); do
    ready="$(sudo docker node inspect -f {{.Status.State}} $id)"
    active="$(sudo docker node inspect -f {{.Spec.Availability}} $id)"
    nodeip="$(sudo docker node inspect -f {{.Status.Addr}} $id)"
    labels="$(sudo docker node inspect -f {{.Spec.Labels}} $id)"
    role="$(sudo docker node inspect -f {{.Spec.Role}} $id)"

    # skip unavailable or manager node
    if test "$ready" = "ready"; then
        if test "$active" = "active"; then
            if test -z "$(hostname -I | grep --fixed-strings $nodeip)"; then

                for image in $(awk -v constraints=1 -v role="node.role==${role}" -v labels="$labels" -f "$DIR/scan-yml.awk" "$YML"); do

                    # trasnfer VCAC-A images to VCAC-A nodes only
                    if test -n "$(echo $nodeip | grep --fixed-strings 172.32.1.1)"; then
                        transfer_image $image "root@$nodeip"
                    else
                        if test -z "$passwd"; then
                            read -p "Sudo password for workers: " -s passwd
                            echo
                        fi
                        transfer_image $image "$(id -un)@$nodeip" $passwd
                    fi

                done

            fi
        fi
    fi
done
