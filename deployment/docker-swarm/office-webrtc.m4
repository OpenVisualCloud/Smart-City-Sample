
define(`UDPBASE',ifdef(`UDPBASE',defn(`UDPBASE'),0))dnl

    defn(`OFFICE_NAME')_webrtc:
        image: IMAGENAME(smtc_sensor_webrtc)
        command: [ "/home/launch.sh","webrtc","/home/webs.py" ]
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')_db):9200"
            `WEBRTC_STREAMING_LIMIT': "defn(`WEBRTC_STREAMING_LIMIT')"
            `WEBRTC_UDP_PORT': "eval(defn(`WEBRTC_UDP_PORT')+defn(`UDPBASE'))"
            INACTIVE_TIME: "10"
            WEBRTC_HOSTIP: "defn(`HOSTIP')"
            WEBRTC_MQ_HOST: "defn(`OFFICE_NAME')_rabbitmq"
            WEBRTC_DB_HOST: "defn(`OFFICE_NAME')_mongodb"
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
        deploy:
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes

    defn(`OFFICE_NAME')_rabbitmq:
        image: IMAGENAME(smtc_sensor_webrtc)
        command: [ "/home/launch.sh","rabbitmq" ]
        environment:
            RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS: "+sbwt none"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        user: rabbitmq
        deploy:
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes

    defn(`OFFICE_NAME')_mongodb:
        image: IMAGENAME(smtc_sensor_webrtc)
        command: [ "/home/launch.sh","mongodb" ]
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        user: mongodb
        deploy:
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes

define(`UDPBASE',eval(defn(`UDPBASE')+defn(`WEBRTC_STREAMING_LIMIT')))dnl

