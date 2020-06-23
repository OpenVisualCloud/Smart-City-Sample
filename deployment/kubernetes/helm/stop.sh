#!/bin/bash

DIR=$(dirname $(readlink -f "$0"))

shift
. "$DIR/build.sh"

helm uninstall smtc${SCOPE}

case "N$SCOPE" in
    N | Ncloud)
        kubectl delete secret self-signed-certificate 2> /dev/null
        kubectl delete configmap sensor-info 2> /dev/null
        ;;
esac

echo -n ""
