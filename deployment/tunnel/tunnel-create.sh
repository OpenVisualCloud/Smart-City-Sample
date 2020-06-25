#!/bin/bash -e

for env1 in $(env); do 
    name="$(echo $env1 | cut -f1 -d=)"
    value="$(echo $env1 | cut -f2 -d=)"
    src_host="$(echo $value | cut -f1 -d' ')"
    dst_host="$(echo $value | cut -f2 -d' ')"
    case "$name" in
       FORWARD_TUNNEL*)
           ssh -i /mnt/id_rsa -o StrictHostKeyChecking=no -f -N -L $(echo $src_host|cut -f2 -d:):$dst_host $(echo $src_host | cut -f1 -d:)
           ;;
       REVERSE_TUNNEL*)    
           ssh -i /mnt/id_rsa -o StrictHostKeyChecking=no -f -N -R $(echo $src_host|cut -f2 -d:):$dst_host $(echo $src_host | cut -f1 -d:)
           ;;
    esac
done

exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
