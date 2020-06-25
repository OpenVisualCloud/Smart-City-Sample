#!/bin/bash

IFS=$(echo -en "\n\b")

for env1 in $(env); do
    case "$env1" in
    WAIT_SOURCE*)
        value="$(echo $env1 | cut -f2 -d=)"
        while true; do
            echo curl -sSf $value
            curl -sSf $value && break
            sleep 1
        done
        ;;
    esac
done

for env1 in $(env); do 
    value="$(echo $env1 | cut -f2 -d=)"
    remote_host="$(echo $value | cut -f1 -d' ')"
    local_host="$(echo $value | cut -f2- -d' ')"
    remote_port="$(echo $remote_host | cut -f2- -d':')"
    remote_host="$(echo $remote_host | cut -f1 -d':')"

    case "$env1" in
    FORWARD_TUNNEL*)
        echo ssh -i /mnt/id_rsa -o StrictHostKeyChecking=no -f -N -L "$remote_port:$local_host" "$remote_host"
        ssh -i /mnt/id_rsa -o StrictHostKeyChecking=no -f -N -L "$remote_port:$local_host" "$remote_host"
        ;;
    REVERSE_TUNNEL*)    
        echo "value=$value"
        echo "remote_host=$remote_host"
        echo "local_host=$local_host"
        echo ssh -i /mnt/id_rsa -o StrictHostKeyChecking=no -f -N -R "$remote_port:$local_host" "$remote_host"
        ssh -i /mnt/id_rsa -o StrictHostKeyChecking=no -f -N -R "$remote_port:$local_host" "$remote_host"
        ;;
    esac
done

exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
