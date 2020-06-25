#!/bin/bash -e

# create key pair for ssh to cloud db host machine
if [ ! -f /home/.key/id_rsa ]; then
    rm -rf "/home/.key"
    mkdir "/home/.key"
    ssh-keygen -f /home/.key/id_rsa -N "" -q
    # copy keys to cloud db host machine
    ssh-copy-id -i /home/.key/id_rsa -o StrictHostKeyChecking=no $1
fi
