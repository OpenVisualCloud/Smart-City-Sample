#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="${4:-1}"

shift
. "$DIR/build.sh"

function create_secret {
    kubectl create secret generic self-signed-certificate "--from-file=${DIR}/../../certificate/self.crt" "--from-file=${DIR}/../../certificate/self.key"
}

case "N$SCOPE" in
    N | Ncloud)
        # create secrets
        "$DIR/../../certificate/self-sign.sh"
        create_secret 2>/dev/null || (kubectl delete secret self-signed-certificate; create_secret)

        # create configmap
        kubectl create configmap sensor-info "--from-file=${DIR}/../../../maintenance/db-init/sensor-info.json"
        ;;
esac

for yaml in $(find "$DIR" -maxdepth 1 -name "*.yaml" -print); do
    kubectl apply -f "$yaml" 2>&1 | grep -v "no objects passed to apply" || echo -n ""
done
