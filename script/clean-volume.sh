#!/bin/bash -e

if test -z "$1"; then
    echo "Usage: <host|user@host> [...]"
    exit -1
fi

storage="/mnt/storage"
hostname="$(hostname)"
for host1 in "$@"; do
    case "$host1" in
    *$hostname*)
        echo "$host1:${storage}"
        rm -rf "${storage}/*" || echo
        ;;
    *)
        echo "$host1:${storage}"
        ssh "$host1" rm -rf "${storage}/*" || echo
        ;;
    esac
done
