#!/bin/bash -e

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
                if [[ -n $(awk -v constraints=1 -v role="node.role==${role}" -v labels="$labels" -f "$DIR/scan-yml.awk" "$YML") ]]; then

                    if test -n "$(echo $nodeip | grep --fixed-strings 172.32.1.1)"; then
                    
                        ssh root@$nodeip "docker container prune -f"
                        ssh root@$nodeip "docker volume prune -f"
                        ssh root@$nodeip "docker network prune -f"

                    else

                        if test -z "$passwd"; then
                            read -p "Sudo password for workers: " -s passwd
                            echo
                        fi

                        echo $passwd | ssh "$nodeip" sudo --prompt="" -S -- "docker container prune -f"
                        echo $passwd | ssh "$nodeip" sudo --prompt="" -S -- "docker volume prune -f"
                        echo $passwd | ssh "$nodeip" sudo --prompt="" -S -- "docker network prune -f"

                    fi

                fi
            else

                sudo docker container prune -f
                sudo docker volume prune -f
                sudo docker network prune -f

            fi
        fi
    fi
done
