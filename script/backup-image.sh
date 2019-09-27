#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
YML="$DIR/../deployment/docker-swarm/docker-compose.yml"

mkdir -p "$DIR/../archive"
for image in `awk -v 'labels=*' -f "$DIR/scan-yaml.awk" "$YML"` smtc_certificate:latest; do
    imagefile=${image//\//-}
    imagefile=${imagefile//:/-}
    echo "archiving $image => $imagefile"
    (docker image save "$image" > "$DIR/../archive/${imagefile}.tar") || (docker pull "$image" && (docker image save "$image" > "$DIR/../archive/${imagefile}.tar"))
done

