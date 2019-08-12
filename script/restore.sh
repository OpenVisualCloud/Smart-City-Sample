#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

if test -z "$1"; then
    echo "Usage: <host|user@host> [...]"
    exit -1
fi

hostname="$(hostname)"
pw=""
for host1 in "$@"; do
    echo "Transfer images to $host1"
    for tarfile in "$DIR/../archive"/*.tar; do
        case "$host1" in
        *$hostname*)
            sudo docker load -i "$tarfile"
            ;;
        *)
            if test -z "$pw"; then
                read -p "Sudo password: " -s pw
                echo
            fi
            # assume the host can ssh to host1 without password
            echo $pw | cat - $tarfile | ssh $host1 cat \| sudo --prompt="" -S -- "docker load"
            ;;
        esac
    done
done
