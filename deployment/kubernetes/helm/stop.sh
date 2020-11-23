#!/bin/bash

DIR=$(dirname $(readlink -f "$0"))

helm uninstall smtc${SCOPE}

case "N$SCOPE" in
    N | Ncloud)
        kubectl delete secret self-signed-certificate 2> /dev/null
        ;;
esac

kubectl delete configmap sensor-info 2> /dev/null

if [ -n "${CONNECTOR_CLOUD}" ]; then
    case "N$SCOPE" in
        Ncloud | Noffice*-svc | Noffice*-camera | Noffice*)
            kubectl delete secret tunnel-secret 2> /dev/null
        ;;
    esac
fi

echo -n ""
