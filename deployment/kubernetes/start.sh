#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="${4:-1}"

export USER_ID="$(id -u)"
export GROUP_ID="$(id -g)"

if test -n "$1"; then shift; fi
. "$DIR/build.sh"

"$DIR/../certificate/self-sign.sh"
kubectl create secret generic self-signed-certificate --from-file=../certificate/dhparam.pem  --from-file=../certificate/self.crt --from-file=../certificate/self.key
for yaml in $(find "$DIR" -maxdepth 1 -name "*.yaml" -print); do
    kubectl apply -f "$yaml"
done
