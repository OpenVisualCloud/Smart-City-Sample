#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

if test -z "$1"; then
    for tarfile in "$DIR/../archive"/*.tar; do
        sudo docker load -i "$tarfile"
    done
else
    read -p "Password: " -s pw
    echo
    for host1 in "$@"; do
        echo "Transfer images to $host1"
        for tarfile in "$DIR/../archive"/*.tar; do
            # assume the host can ssh to host1 without password
            echo $pw | cat - $tarfile | ssh $host1 cat \| sudo --prompt="" -S -- "docker load"
        done
    done
fi
