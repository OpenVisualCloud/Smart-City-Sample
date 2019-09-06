#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
YML="$DIR/../deployment/docker-swarm/docker-compose.yml"

mkdir -p "$DIR/../archive"
for image in `awk '/image:/{print $2}/docker run/{im=$NF;gsub(/\"/,"",im);print im}' "$YML"` smtc_certificate:latest; do
    imagefile=${image//\//-}
    imagefile=${imagefile//:/-}
    echo "archiving $image => $imagefile"
    (sudo docker image save "$image" > "$DIR/../archive/${imagefile}.tar") || (sudo docker pull "$image" && (sudo docker image save "$image" > "$DIR/../archive/${imagefile}.tar"))
done

