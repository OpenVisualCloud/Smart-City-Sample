#!/bin/bash

DIR=$(dirname $(readlink -f "$0"))

helm uninstall smtc${SCOPE}

case "N$SCOPE" in
    N | Ncloud)
        kubectl delete secret self-signed-certificate 2> /dev/null
        ;;
esac

kubectl delete configmap sensor-info 2> /dev/null

echo -n ""
