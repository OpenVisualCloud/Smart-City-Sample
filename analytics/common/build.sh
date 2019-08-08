#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

USER="docker"
GROUP="docker"

case "$1" in 
    vcac-a)
        PLATFORM=VCAC-A
        ;;
    *)
        PLATFORM=Xeon
        ;;
esac

# build image(s) in order (to satisfy dependencies)
for dep in '.8.*' '.7.*' '.6.*' '.5.*' '.4.*' '.3.*' '.2.*' '.1.*' ''; do
    for dockerfile in `find "${DIR}/platforms/${PLATFORM}" -maxdepth 1 -name "Dockerfile${dep}" -print`; do
        image=$(head -n 1 "$dockerfile" | grep '# ' | cut -d' ' -f2)
        if test -z "$image"; then image="$IMAGE"; fi

        if grep -q 'AS build' "$dockerfile"; then
            echo sudo docker build --file="$dockerfile" --target build -t "$image:build" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)
            sudo docker build --file="$dockerfile" --target build -t "$image:build" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)
        fi

        echo sudo docker build --file="$dockerfile" -t "$image:latest" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)
        sudo docker build --file="$dockerfile" -t "$image:latest" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=${USER} --build-arg GROUP=${GROUP} --build-arg UID=$(id -u) --build-arg GID=$(id -g)
    done
done
