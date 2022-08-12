#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
. "$DIR/config.sh" WEBRTC_

configure_webrtc_agent () {
    # patch webrtc agent
    eth=$(ip route get 8.8.8.8 | cut -f5 -d' ' | head -n 1)
    sed -i "s/^network_interfaces = .*/network_interfaces =[{ name=\"$eth\", replaced_ip_address=\"$WEBRTC_HOSTIP\"}]/" /home/owt/webrtc_agent/agent.toml
    
    let minport=$WEBRTC_UDP_PORT+1
    sed -i "/webrtc/,\$s/^minport =.*/minport = $minport/" /home/owt/webrtc_agent/agent.toml
    let maxport=$WEBRTC_UDP_PORT+$WEBRTC_STREAMING_LIMIT
    sed -i "/webrtc/,\$s/^maxport =.*/maxport = $maxport/" /home/owt/webrtc_agent/agent.toml
}

configure_owt_api_py () {
    # patch owtapi.py
    ( cd /home/owt; ./management_api/init.sh )
    service=$(grep API.init /home/owt/apps/current_app/main.js | cut -d"'" -f2)
    key=$(grep API.init /home/owt/apps/current_app/main.js | cut -d"'" -f4 | sed 's/\//\\\//g')
    sed -i "s/service=''/service='${service}'/" /home/owtapi.py
    sed -i "s/key=''/key='${key}'/" /home/owtapi.py
}

configure_mq_if_needed() {
    if [ -z $WEBRTC_MQ_HOST ];then
        return
    fi
    configure_mq_host /home/owt/management_api/management_api.toml
    configure_mq_host /home/owt/cluster_manager/cluster_manager.toml
    configure_mq_host /home/owt/portal/portal.toml
    configure_mq_host /home/owt/conference_agent/agent.toml
    configure_mq_host /home/owt/audio_agent/agent.toml
    configure_mq_host /home/owt/video_agent/agent.toml
    configure_mq_host /home/owt/webrtc_agent/agent.toml
    configure_mq_host /home/owt/streaming_agent/agent.toml
}
configure_mq_host () {
    sed -i "s/^host = \"localhost\" .*/host = \"$WEBRTC_MQ_HOST\"/" $1
    echo "update $1 mq host = $WEBRTC_MQ_HOST"
}
configure_db_if_needed() {
    if [ -z $WEBRTC_DB_HOST ];then
        return
    fi
    configure_db_host /home/owt/management_api/management_api.toml
    configure_db_host /home/owt/portal/portal.toml
    configure_db_host /home/owt/conference_agent/agent.toml
}
configure_db_host() {
    sed -i "s/^dataBaseURL = \"localhost/dataBaseURL = \"$WEBRTC_DB_HOST/" $1
    echo "update $1 db host = $WEBRTC_DB_HOST"
}

wait_for_mongod () {
    hostinfo=
    if [[ ! -z $WEBRTC_DB_HOST ]];then
        hostinfo="--host $WEBRTC_DB_HOST"
    fi
    while ! mongo $hostinfo --quiet --eval "db.adminCommand('listDatabases')"; do
        echo Waiting for monogod
        sleep 1
    done
    echo mongodb connected successfully
}

configure_rabbitmq_user_profile () {
    echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config
}

configure_hw_acceleration () {
    sed -i "s/^hardwareAccelerated = .*/hardwareAccelerated = true/" $1
}

trap 'exit 0' SIGTERM

case "N$1" in
Nrabbitmq)
    configure_rabbitmq_user_profile 
    /usr/sbin/rabbitmq-server &
    ;;
Nmongodb)
    /usr/bin/mongod --config /etc/mongodb.conf &
    ;;
Nwebrtc)

    configure_mq_if_needed
    configure_db_if_needed

    wait_for_mongod
    configure_owt_api_py

    cd /home/owt/bin
    ./daemon.sh start management-api
    ./daemon.sh start cluster-manager
    ./daemon.sh start portal
    ./daemon.sh start conference-agent
    ./daemon.sh start audio-agent
    configure_hw_acceleration /home/owt/video_agent/agent.toml
    ./daemon.sh start video-agent

    configure_webrtc_agent
    ./daemon.sh start webrtc-agent
    ./daemon.sh start streaming-agent
    ;;
esac

if [ -z "$2" ]; then
    while true; do
       sleep 10000
    done
else
    exec "$2"
fi
