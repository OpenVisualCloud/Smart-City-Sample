#!/bin/bash -e

if test -z "$1"; then
    echo "Usage: [<user>] </mnt/storage>"
    exit -1
fi

if test -z "$2"; then
    user="$(id -un)"
    storage="$1"
else
    user="$1"
    storage="$2"
fi

domain=$(hostname -d)
for host1 in `sudo docker node ls --filter role=worker --format "{{.Hostname}} {{.Availability}}" | grep Active | cut -f1 -d' '`; do
    user1="$user"
    if test "$host1" = "$(hostname)"; then
        user1="$(id -un)"
    fi
    echo "$user1@$host1.$domain:$storage"
    ssh "$user1@$host1.$domain" rm -rf "$storage/*" || echo
done
