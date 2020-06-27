#!/bin/bash -e

case "$(cat /proc/1/sched | head -n 1)" in
*create-key.sh*)  # in docker

    # create key pair for ssh to cloud db host machine
    if [ ! -f /home/.key/id_rsa ]; then
        rm -rf "/home/.key"
        mkdir "/home/.key"
        ssh-keygen -f /home/.key/id_rsa -N "" -q
    fi

    # copy keys to cloud db host machine
    ssh-copy-id -i /home/.key/id_rsa -o StrictHostKeyChecking=no "$1"
    ;;
*)
    IMAGE="smtc_web_cloud_tunnelled"
    DIR=$(dirname $(readlink -f "$0"))
    OPTIONS=(-v "$DIR:/home:rw")
    . "$DIR/../../script/shell.sh" /home/create-key.sh "$1"
    ;;
esac
