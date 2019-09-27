#!/bin/bash -e

echo "Looking for cloud-web-service..."
for i in 1 2 3 4 5 6 7 8 9 10; do
    if test -n "$(kubectl get services cloud-web-service 2>/dev/null)"; then
        hostip=$(hostname -I | cut -f1 -d' ')
        kubectl patch svc cloud-web-service -p "{\"spec\":{\"externalIPs\":[\"$hostip\"]}}"
        echo "patched to http://$hostip:8443"
        exit 0
    fi
    sleep 2
done
echo "Failed to identify Looking for cloud-web-service..."
