
define(`UDPBASE',ifdef(`UDPBASE',defn(`UDPBASE'),0))dnl

    defn(`OFFICE_NAME')_webrtc:
        image: defn(`REGISTRY_PREFIX')smtc_sensor_webrtc:latest
        command: [ "/bin/bash","-c","service mongodb start && service rabbitmq-server start && exec /home/launch.sh /home/webs.py" ]
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')_db):9200"
            `WEBRTC_STREAMING_LIMIT': "defn(`WEBRTC_STREAMING_LIMIT')"
            `WEBRTC_UDP_PORT': "eval(defn(`WEBRTC_UDP_PORT')+defn(`UDPBASE'))"
            INACTIVE_TIME: "10"
            WEBRTC_HOSTIP: "defn(`HOSTIP')"
            RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS: "+sbwt none"
            NO_PROXY: "*"
            no_proxy: "*"
        ports:
loop(PORTIDX,1,defn(`WEBRTC_STREAMING_LIMIT'),`dnl
            - target: eval(defn(`WEBRTC_UDP_PORT')+defn(`UDPBASE')+defn(`PORTIDX'))
              published: eval(defn(`WEBRTC_UDP_PORT')+defn(`UDPBASE')+defn(`PORTIDX'))
              protocol: udp
              mode: host
')dnl
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        user: root
        deploy:
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes

define(`UDPBASE',eval(defn(`UDPBASE')+defn(`WEBRTC_STREAMING_LIMIT')))dnl

