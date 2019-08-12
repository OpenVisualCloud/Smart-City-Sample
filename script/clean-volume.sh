#!/bin/bash -e

if test -z "$1"; then
    echo "Usage: [<user>]"
    exit -1
fi

if test -z "$1"; then
    user="$(id -un)"
else
    user="$1"
fi

storage="/mnt/storage"
domain=$(hostname -d)
for host1 in `sudo docker node ls --format "{{.Hostname}} {{.Availability}}" | grep Active | cut -f1 -d' '`; do
    user1="$user"
    if test "$host1" = "$(hostname)"; then
        echo "$(id -un)@$host1.$domain:${storage}"
        rm -rf "${storage}/*" || echo
    else
        echo "$user1@$host1.$domain:${storage}"
        ssh "$user1@$host1.$domain" rm -rf "${storage}/*" || echo
    fi
done
