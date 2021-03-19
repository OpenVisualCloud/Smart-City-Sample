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

wait_for_mongod () {
    while ! mongo --quiet --eval "db.adminCommand('listDatabases')"; do
        echo Waiting for monogod
        sleep 1
    done
    echo mongodb connected successfully
}

configure_hw_acceleration () {
    sed -i "s/^hardwareAccelerated = .*/hardwareAccelerated = true/" $1
}

trap 'exit 0' SIGTERM

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

exec "$1"
