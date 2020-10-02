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
    service=$(grep API.init /home/owt/extras/basic_example/samplertcservice.js | cut -d"'" -f2)
    key=$(grep API.init /home/owt/extras/basic_example/samplertcservice.js | cut -d"'" -f4 | sed 's/\//\\\//g')
    sed -i "s/service=''/service='${service}'/" /home/owtapi.py
    sed -i "s/key=''/key='${key}'/" /home/owtapi.py
}

configure_comm_host () {
    sed -i "s/^host = \"localhost\" .*/host = \"$WEBRTC_COMM_HOST\"/" $1
}

wait_for_mongod () {
    while ! mongo --quiet --eval "db.adminCommand('listDatabases')"; do
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
Ncomm)
    configure_rabbitmq_user_profile 
    service rabbitmq-server start &
    ;;
Ncontrol)
    service mongodb start &

    wait_for_mongod
    configure_owt_api_py

    cd /home/owt/bin
    configure_comm_host /home/owt/management_api/management_api.toml
    ./daemon.sh start management-api
    configure_comm_host /home/owt/cluster_manager/cluster_manager.toml
    ./daemon.sh start cluster-manager
    configure_comm_host /home/owt/portal/portal.toml
    ./daemon.sh start portal
    configure_comm_host /home/owt/conference_agent/agent.toml
    ./daemon.sh start conference-agent
    ;;
Ntranscode)
    cd /home/owt/bin
    configure_comm_host /home/owt/audio_agent/agent.toml
    ./daemon.sh start audio-agent
    configure_comm_host /home/owt/video_agent/agent.toml
    configure_hw_acceleration /home/owt/video_agent/agent.toml
    ./daemon.sh start video-agent
    ;;
Nio)
    configure_webrtc_agent

    cd /home/owt/bin
    configure_comm_host /home/owt/webrtc_agent/agent.toml
    ./daemon.sh start webrtc-agent
    configure_comm_host /home/owt/streaming_agent/agent.toml
    ./daemon.sh start streaming-agent
    ;;
N)
    service rabbitmq-server start &
    service mongodb start &

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
