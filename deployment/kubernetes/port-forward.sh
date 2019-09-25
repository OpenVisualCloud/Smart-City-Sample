#!/bin/bash -e

case "$1" in
start)
    echo "Looking for cloud-web-service..."
    for i in 1 2 3 4 5 6 7 8 9 10; do
        pod=$(kubectl get pods | grep Running | grep cloud-web | cut -f1 -d' ')
        if test -n "$pod"; then
            sudo kubectl port-forward pod/$pod 443:8443 --address 0.0.0.0 > /dev/null 2> /dev/null &
            exit 0
        fi
        sleep 2
    done
    echo "Failed to identify Looking for cloud-web-service..."
    ;;
stop)
    sudo kill $(sudo ps aux | awk '/kubectl port-forward/{print$2}')
    ;;
*)
    echo "Usage: <start|stop>"
    ;;
esac
