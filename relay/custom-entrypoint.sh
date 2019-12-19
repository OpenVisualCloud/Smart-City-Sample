#!/bin/bash -e
for ((i = 1; i <= $RELAY_NUMBER; i++))
do
    eval src_host=\${RELAY${i}_SRC_HOST}
    eval src_port=\${RELAY${i}_SRC_PORT}
    eval dst_host=\${RELAY${i}_DST_HOST}
    eval dst_port=\${RELAY${i}_DST_PORT}
    ssh -i /etc/relay-key-pair/relay-key -o StrictHostKeyChecking=no -f -N -R "$src_port:$dst_host:$dst_port" $src_host
done

exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"

