#!/bin/bash -e
service mongodb start &
service rabbitmq-server start &
while ! mongo --quiet --eval "db.adminCommand('listDatabases')"
do
  echo mongod not launch
  sleep 1
done
echo mongodb connected successfully

eth=$(ip route get 8.8.8.8 | cut -f5 -d' ' | head -n 1)
sed -i "s/^network_interfaces = .*/network_interfaces =[{ name=\"$eth\", replaced_ip_address=\"$WEBRTC_HOSTIP\"}]/" /home/owt/webrtc_agent/agent.toml

let minport=$WEBRTC_UDP_PORT+1
sed -i "/webrtc/,\$s/^minport =.*/minport = $minport/" /home/owt/webrtc_agent/agent.toml
let maxport=$WEBRTC_UDP_PORT+$STREAMING_LIMIT
sed -i "/webrtc/,\$s/^maxport =.*/maxport = $maxport/" /home/owt/webrtc_agent/agent.toml

cd /home/owt
./management_api/init.sh

service=$(grep API.init /home/owt/extras/basic_example/samplertcservice.js | cut -d"'" -f2)
key=$(grep API.init /home/owt/extras/basic_example/samplertcservice.js | cut -d"'" -f4 | sed 's/\//\\\//g')
sed -i "s/service=''/service='${service}'/" /home/owtapi.py
sed -i "s/key=''/key='${key}'/" /home/owtapi.py

cd /home/owt/bin
./daemon.sh start management-api $1
./daemon.sh start cluster-manager $1
./daemon.sh start portal $1
./daemon.sh start audio-agent $1
./daemon.sh start streaming-agent $1
./daemon.sh start conference-agent $1
./daemon.sh start video-agent $1
./daemon.sh start webrtc-agent $1
