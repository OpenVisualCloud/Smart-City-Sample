#!/bin/bash -e

case "$(cat /proc/1/sched | head -n 1)" in
*create-key.sh*)  # in docker
    rm -rf /home/.ssh && mkdir -p /home/.ssh && chmod 700 /home/.ssh

    # create key pair for ssh to cloud db host machine
    if [ ! -f /home/.key/id_rsa ]; then
        rm -rf "/home/.key" && mkdir -p "/home/.key" && chmod 700 /home/.key
        ssh-keygen -f /home/.key/id_rsa -N "" -q
    fi

    # copy keys to cloud db host machine
    ssh-copy-id -o CheckHostIP=yes -o StrictHostKeyChecking=ask -o UserKnownHostsFile=/home/.ssh/known_hosts -i /home/.key/id_rsa "$1"
    ;;
*)
    DIR=$(dirname $(readlink -f "$0"))
    . "$DIR/shell.sh" /home/create-key.sh "$1"
    ;;
esac
