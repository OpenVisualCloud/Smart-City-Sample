#!/bin/bash -e

if test -z "${DIR}"; then 
    echo "This script should not be called directly."
    exit -1
fi 

PLATFORM="${1:-Xeon}"
FRAMEWORK="${6:-gst}"
REGISTRY="${8:-}"

build_docker() {
    docker_file="$1"
    shift
    image_name="$1"
    shift
    if test -f "$docker_file.m4"; then
        m4 -I "$(dirname $docker_file)" "$docker_file.m4" > "$docker_file"
    fi
    (cd "$DIR"; docker build --network host --file="$docker_file" "$@" -t "$image_name" "$DIR" $(env | cut -f1 -d= | grep -E '_(proxy|REPO|VER)$' | sed 's/^/--build-arg /') --build-arg UID=$(id -u) --build-arg GID=$(id -g))

    # if REGISTRY is specified, push image to the private registry
    if [ -n "$REGISTRY" ]; then
        docker tag "$image_name" "$REGISTRY$image_name"
        docker push "$REGISTRY$image_name"
    fi
}

# build image(s) in order (to satisfy dependencies)
for dep in '.5.*' '.4.*' '.3.*' '.2.*' '.1.*' '.0.*' ''; do
    dirs=("$DIR/$PLATFORM/$FRAMEWORK" "$DIR/$PLATFORM" "$DIR")
    for dockerfile in $(find "${dirs[@]}" -maxdepth 1 -name "Dockerfile$dep" -print 2>/dev/null); do
        image=$(head -n 1 "$dockerfile" | grep '# ' | cut -d' ' -f2)
        if test -z "$image"; then image="$IMAGE"; fi
        build_docker "$dockerfile" "$image"
    done
done
