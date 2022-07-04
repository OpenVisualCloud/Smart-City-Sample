#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
REGISTRY="$9"

function create_secret {
    kubectl create secret generic $1 "--from-file=$2" "--from-file=$3"
}

case "N$SCOPE" in
    N | Ncloud)
        # create secrets
        create_secret self-signed-certificate "${DIR}/../certificate/self.crt" "${DIR}/../certificate/self.key"
        ;;
esac

# create configmap
kubectl create configmap sensor-info "--from-file=${DIR}/../../maintenance/db-init/sensor-info.json" || echo -n ""

helm version >/dev/null 2>/dev/null && (
    helm install smtc${SCOPE} "$DIR/helm" --set buildScope=${SCOPE}
) || (
    kubectl apply -f <(docker run --rm -v "$DIR/helm":/apps:ro alpine/helm template smtc /apps --set buildScope=$SCOPE)
)
