#!/bin/bash -e

storage="/mnt/storage"
for id in $(sudo docker node ls -q); do
    ready="$(sudo docker node inspect -f {{.Status.State}} $id)"
    active="$(sudo docker node inspect -f {{.Spec.Availability}} $id)"
    nodeip="$(sudo docker node inspect -f {{.Status.Addr}} $id)"

    if test "$ready" = "ready"; then
        if test "$active" = "active"; then

            if test -z "$(hostname -I | grep --fixed-strings $nodeip)"; then

                worker="$(id -un)@$nodeip"
                if test -n "$(echo $nodeip | grep --fixed-strings 172.32.1.1)"; then
                    worker="root@$nodeip"
                fi

                echo "$worker:${storage}"
                ssh "$worker" "find -L \"${storage}\" -maxdepth 1 -mindepth 1 -type d -exec rm -rf \"{}\" \\; -print"

            else 

                echo "$nodeip:${storage}"
                find -L "${storage}" -maxdepth 1 -mindepth 1 -type d -exec rm -rf "{}" \; -print

            fi
        fi
    fi
done
