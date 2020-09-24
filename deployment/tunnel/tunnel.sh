#!/bin/bash -e

function gracefully_exit {
    exit 0
}

# gracefully exit
trap gracefully_exit SIGTERM

IFS=$(echo -en "\n\b")
mkdir -p ~/.ssh && chmod 700 ~/.ssh
cp -f /etc/hostkey/known_hosts /etc/hostkey/id_rsa ~/.ssh
chmod 400 ~/.ssh/id_rsa ~/.ssh/known_hosts

for env1 in $(env); do 
    value="$(echo $env1 | cut -f2 -d=)"
    remote_host="$(echo $value | cut -f1 -d' ')"
    local_host="$(echo $value | cut -f2- -d' ')"
    remote_port="$(echo $remote_host | cut -f2- -d':')"
    remote_host="$(echo $remote_host | cut -f1 -d':')"

    case "$env1" in
    FORWARD_TUNNEL*)
        echo ssh -o TCPKeepAlive=yes -4 -f -N -L "$local_host:localhost:$remote_port" "$remote_host"
        ssh -o TCPKeepAlive=yes -4 -f -N -L "$local_host:localhost:$remote_port" "$remote_host"
        ;;
    REVERSE_TUNNEL*)    
        echo ssh -o TCPKeepAlive=yes -4 -f -N -R "$remote_port:$local_host" "$remote_host"
        ssh -o TCPKeepAlive=yes -4 -f -N -R "$remote_port:$local_host" "$remote_host"
        ;;
    esac
done

while true; do
    sleep 10000
done
