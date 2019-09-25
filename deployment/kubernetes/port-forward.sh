#!/bin/bash -e

echo "Looking for cloud-web-service..."
for i in 1 2 3 4 5 6 7 8 9 10; do
    pod=$(kubectl get pods | grep Running | grep cloud-web | cut -f1 -d' ')
    if test -n "$pod"; then
        sudo kubectl port-forward pod/$pod 443:8443 --address 0.0.0.0
        exit 0
    fi
    sleep 2
done
echo "Failed to identify Looking for cloud-web-service..."
