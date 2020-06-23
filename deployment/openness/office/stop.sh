#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

shift
. "$DIR/build.sh"

for yaml in $(find "${DIR}" -maxdepth 1 -name "*.yaml" -print); do
    kubectl delete --wait=false -f "$yaml" --ignore-not-found=true 2>/dev/null | grep -v "No resources found"
done
kubectl delete secret relay-key-pair-secret 2> /dev/null || echo -n ""
kubectl delete configmap sensor-info 2> /dev/null || echo -n ""
