#!/bin/bash

DIR=$(dirname $(readlink -f "$0"))

shift
. "$DIR/build.sh"

helm uninstall smtc${SCOPE}

case "N$SCOPE" in
    N | Ncloud)
        kubectl delete secret self-signed-certificate 2> /dev/null
        ;;
esac

kubectl delete configmap sensor-info 2> /dev/null

if [ -n "${CONNECTOR_CLOUD}" ]; then
    case "N$SCOPE" in
        Ncloud | Noffice*)
            kubectl delete secret tunnel-secret 2> /dev/null
        ;;
    esac
fi

echo -n ""
