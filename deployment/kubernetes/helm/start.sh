#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
REGISTRY="$9"

function create_secret {
    kubectl create secret generic $1 "--from-file=$2" "--from-file=$3"
}

function create_secret2 {
    kubectl create secret generic $1 "--from-file=$2" "--from-file=$3" "--from-file=$4" 2> /dev/null || (kubectl delete secret $1; kubectl create secret generic $1 "--from-file=$2" "--from-file=$3" "--from-file=$4")
}

case "N$SCOPE" in
    N | Ncloud)
        # create secrets
        create_secret self-signed-certificate "${DIR}/../../certificate/self.crt" "${DIR}/../../certificate/self.key"
        ;;
esac

# create configmap
kubectl create configmap sensor-info "--from-file=${DIR}/../../../maintenance/db-init/sensor-info.json" || echo -n ""

if [ -n "${CONNECTOR_CLOUD}" ]; then
    case "N$SCOPE" in
        Ncloud | Noffice*-svc | Noffice*-camera | Noffice*)
            # create secrets
            "$DIR/../../tunnel/create-key.sh" "${CONNECTOR_CLOUD}" "${REGISTRY}"
            create_secret2 tunnel-secret "${DIR}/../../tunnel/.key/id_rsa" "${DIR}/../../tunnel/.key/id_rsa.pub" "${DIR}/../../tunnel/.ssh/known_hosts"
        ;;
    esac
fi

helm install smtc${SCOPE} "$DIR/smtc" --set buildScope=${SCOPE} --set "connector.cloudHost=${CONNECTOR_CLOUD}" --set "connector.cameraHost=${CONNECTOR_CAMERA}"
