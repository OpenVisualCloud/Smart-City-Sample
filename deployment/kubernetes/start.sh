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

helm install smtc${SCOPE} "$DIR/smtc" --set buildScope=${SCOPE} --set "connector.cloudHost=${CONNECTOR_CLOUD}" --set "connector.cameraHost=${CONNECTOR_CAMERA}"
