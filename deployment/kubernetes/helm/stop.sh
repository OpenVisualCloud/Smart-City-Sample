#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

helm uninstall smtc
kubectl delete secret self-signed-certificate 2> /dev/null || echo -n ""
kubectl delete configmap sensor-info 2> /dev/null || echo -n ""
