#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

for yaml in $(find "${DIR}" -maxdepth 1 -name "*.yaml" -print); do
    kubectl delete -f "$yaml" --ignore-not-found=true 2>/dev/null || echo -n ""
done

kubectl delete configmap sensor-info 2> /dev/null || echo -n ""
kubectl delete secret relay-key-pair-secret 2> /dev/null || echo -n ""
