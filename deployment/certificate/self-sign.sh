#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
USER="docker"
P1=$1    # parameter 1
NOFFICE=$2
SCENARIO_NAME=$3

if [ $# -eq 2 ]; then
    P1=""
    NOFFICE=$1
    SCENARIO_NAME=$2
fi

function mqtt_cert(){
    SUBJ_SERVER_INFO="/C=US/ST=Oregon/L=Portland/O=Intel Corporation/OU=SERVER/CN=$2"
    SUBJ_CLIENT_INFO="/C=US/ST=Oregon/L=Portland/O=Intel Corporation/OU=CLIENT/CN=$2"

    CUR_FOLDER=/home/$USER/office$1
    mkdir -p $CUR_FOLDER

    # server
    openssl req -nodes -sha256 -new -subj "$SUBJ_SERVER_INFO" -keyout $CUR_FOLDER/mqtt_server.key -out $CUR_FOLDER/mqtt_server.csr
    openssl x509 -req -sha256 -days 30 -CA /home/$USER/self.crt -CAkey /home/$USER/self.key \
        -in $CUR_FOLDER/mqtt_server.csr -CAcreateserial -out $CUR_FOLDER/mqtt_server.crt
    
    # client
    openssl req -new -nodes -sha256 -subj "$SUBJ_CLIENT_INFO" -keyout $CUR_FOLDER/mqtt_client.key -out $CUR_FOLDER/mqtt_client.csr 
    openssl x509 -req -sha256 -days 30 -CA /home/$USER/self.crt -CAkey /home/$USER/self.key \
        -in $CUR_FOLDER/mqtt_client.csr -CAcreateserial -out $CUR_FOLDER/mqtt_client.crt

    chmod 644 $CUR_FOLDER/mqtt_server.key
    chmod 644 $CUR_FOLDER/mqtt_server.crt
    chmod 644 $CUR_FOLDER/mqtt_client.key
    chmod 644 $CUR_FOLDER/mqtt_client.crt
    rm -f $CUR_FOLDER/*.csr
}

case "$(cat /proc/1/sched | head -n 1)" in
*self-sign*)
    SUBJ_CA_INFO="/C=US/ST=Oregon/L=Portland/O=Intel Corporation/OU=Data Center Group/CN=$P1"
    openssl req -x509 -nodes -days 30 -newkey rsa:4096 -subj "$SUBJ_CA_INFO" \
        -keyout /home/$USER/self.key -out /home/$USER/self.crt

    chmod 640 "/home/$USER/self.key"
    chmod 644 "/home/$USER/self.crt"

    for i in `seq 1 $NOFFICE`
    do
        mqtt_cert $i "$SCENARIO_NAME-office$i-mqtt-service"
    done
    ;;
*)
    IMAGE=$P1"smtc_certificate"
    OPTIONS=("--volume=$DIR:/home/$USER:rw")
    . "$DIR/../../script/shell.sh" /home/$USER/self-sign.sh "$(hostname -f)" $NOFFICE $SCENARIO_NAME
    ;;
esac
