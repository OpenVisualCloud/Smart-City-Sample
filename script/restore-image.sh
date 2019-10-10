#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

for tarfile in "$DIR/../archive"/*.tar; do
    docker load -i "$tarfile"
done

