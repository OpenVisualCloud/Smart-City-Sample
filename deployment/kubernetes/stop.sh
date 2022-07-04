#!/bin/bash

DIR=$(dirname $(readlink -f "$0"))

helm version >/dev/null 2>/dev/null && (
    helm uninstall smtc$SCOPE
) || (
    kubectl delete -f <(docker run --rm -v "$DIR/helm":/apps:ro alpine/helm template smtc /apps --set buildScope=$SCOPE)
)

case "N$SCOPE" in
    N | Ncloud)
        kubectl delete secret self-signed-certificate 2> /dev/null
        ;;
esac

kubectl delete configmap sensor-info 2> /dev/null

echo -n ""
