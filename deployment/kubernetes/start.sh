#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NOFFICES="${4:-1}"

shift
. "$DIR/build.sh"

function create_secret {
    kubectl create secret generic self-signed-certificate "--from-file=${DIR}/../certificate/self.crt" "--from-file=${DIR}/../certificate/self.key"
}

# create secrets
"$DIR/../certificate/self-sign.sh"
create_secret 2>/dev/null || (kubectl delete secret self-signed-certificate; create_secret)

# create configmap
kubectl create configmap sensor-info "--from-file=${DIR}/../../maintenance/db-init/sensor-info.json"

for yaml in $(find "$DIR" -maxdepth 1 -name "*.yaml" -print); do
    kubectl apply -f "$yaml"
done

echo "Workaround: Patching cloud-web-service..."
while true; do
    if test -n "$(kubectl get services cloud-web-service 2>/dev/null)"; then
        hostip=$(hostname -i || hostname -I | cut -f1 -d' ')
        kubectl patch svc cloud-web-service -p "{\"spec\":{\"externalIPs\":[\"$hostip\"]}}"
        echo "patched to expose https://$hostip"
        exit 0
    fi
    sleep 2
done
