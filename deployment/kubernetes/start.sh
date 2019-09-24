#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="${4:-1}"

export USER_ID="$(id -u)"
export GROUP_ID="$(id -g)"

if test -n "$1"; then shift; fi
. "$DIR/build.sh"

function create_secret {
    kubectl create secret generic self-signed-certificate "--from-file=${DIR}/../certificate/dhparam.pem" "--from-file=${DIR}/../certificate/self.crt" "--from-file=${DIR}/../certificate/self.key"
}

"$DIR/../certificate/self-sign.sh"
create_secret 2>/dev/null || (kubectl delete secret self-signed-certificate; create_secret)
for yaml in $(find "$DIR" -maxdepth 1 -name "*.yaml" -print); do
    kubectl apply -f "$yaml"
done

