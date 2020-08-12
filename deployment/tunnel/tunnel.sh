#!/bin/bash

IFS=$(echo -en "\n\b")

mkdir -p ~/.ssh && chmod 700 ~/.ssh
for env1 in $(env); do 
    value="$(echo $env1 | cut -f2 -d=)"
    remote_host="$(echo $value | cut -f1 -d' ')"
    local_host="$(echo $value | cut -f2- -d' ')"
    remote_port="$(echo $remote_host | cut -f2- -d':')"
    remote_host="$(echo $remote_host | cut -f1 -d':')"

    case "$env1" in
    FORWARD_TUNNEL*)
        ssh-keyscan -4 ${remote_host/*@/} > ~/.ssh/known_hosts
        echo ssh -4 -f -N -L "$local_host:localhost:$remote_port" "$remote_host"
        printf "yes\nyes\n" | ssh -i /etc/hostkey/id_rsa -4 -f -N -L "$local_host:localhost:$remote_port" "$remote_host"
        ;;
    REVERSE_TUNNEL*)    
        ssh-keyscan -4 ${remote_host/*@/} > ~/.ssh/known_hosts
        echo ssh -4 -f -N -R "$remote_port:$local_host" "$remote_host"
        printf "yes\nyes\n" | ssh -i /etc/hostkey/id_rsa -4 -f -N -R "$remote_port:$local_host" "$remote_host"
        ;;
    esac
done

exec "${@}"
