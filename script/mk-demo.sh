#!/bin/bash -e

case "$0" in
    *mk-demo*)
        DIR=$(dirname $(readlink -f "$0"))
        YML="$DIR/../deployment/docker-swarm/docker-compose.yml"
        rm -rf "$DIR/../dist"
        mkdir -p "$DIR/../dist"
        for image in `awk -v 'labels=*' -f "$DIR/scan-yaml.awk" "$YML"` smtc_certificate:latest; do
            imagefile=${image//\//-}
            imagefile=${imagefile//:/-}
            echo "archiving $image => $imagefile"
            (docker image save "$image" > "$DIR/../dist/${imagefile}.tar") || (docker pull "$image" && (docker image save "$image" > "$DIR/../dist/${imagefile}.tar"))
        done
        (cd "$DIR/.."; tar cvfz "$DIR/../dist/dirs.tgz" script deployment doc CMakeLists.txt README.md maintenance/db-init/sensor-info.* sensor/simulation/*.mp4)
        cp "$0" "$DIR/../dist/restore.sh"
        ;;
    *restore*)
        for tarfile in *.tar; do
            docker load -i "$tarfile"
        done
        tar xvfzm dirs.tgz
        ;;
esac
