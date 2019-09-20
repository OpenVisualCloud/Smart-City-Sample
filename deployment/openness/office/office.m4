    defn(`OFFICE_NAME')_db:
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
        ports:
            - target: defn(`TRANSPORT_PORT')
              published: defn(`TRANSPORT_PORT')
              protocol: tcp
              mode: host
        environment:
            - "cluster.name=db-cluster"
            - "node.name=defn(`OFFICE_NAME')_db"
            - "node.master=false"
            - "node.data=true"
            - "transport.port=defn(`TRANSPORT_PORT')"
            - "transport.publish_host=${CLOUDHOST}"
            - "discovery.zen.minimum_master_nodes=1"
            - "discovery.zen.ping.unicast.hosts=${CLOUDHOST}:9300"
            - "action.auto_create_index=0"
            - "ES_JAVA_OPTS=-Xms4096m -Xmx4096m"
            - "NO_PROXY=*"
            - "no_proxy=*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
            - defn(`OFFICE_NAME')_esdata:/usr/share/elasticsearch/data:rw

    defn(`OFFICE_NAME')_db_init:
        image: smtc_db_init:latest
        environment:
            DBHOST: "http://defn(`OFFICE_NAME')_db:9200"
            OFFICE: "defn(`OFFICE_LOCATION')"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        deploy:
            restart_policy:
                condition: none

    defn(`OFFICE_NAME')_camera_discovery:
        image: smtc_onvif_discovery:latest
        environment:
            IP_SCAN_RANGE: "${CAMERAHOST}"
            PORT_SCAN_RANGE: "eval(10000+defn(`OFFICEIDX')*1000)-eval(10000+defn(`OFFICEIDX')*1000+defn(`NCAMERAS')*100)"
            SIMULATED_CAMERA: "forloop(`cid',1,defn(`NCAMERAS'),`eval(10000+defn(`OFFICEIDX')*1000+defn(`cid')*100-100),')"
            OFFICE: "defn(`OFFICE_LOCATION')"
            LOCATION: "forloop(`cid',1,defn(`NCAMERAS'),`defn(`location_'defn(`OFFICE_NAME')`_camera'defn(`cid')) ')"
            DBHOST: "http://defn(`OFFICE_NAME')_db:9200"
            SERVICE_INTERVAL: "30"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro

    defn(`OFFICE_NAME')_health_check:
        image: smtc_trigger_health
        volumes:
            - /etc/localtime:/etc/localtime:ro
        environment:
            SERVICE_INTERVAL: "300"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://defn(`OFFICE_NAME')_db:9200"
            NO_PROXY: "*"
            no_proxy: "*"

    defn(`OFFICE_NAME')_where_indexing:
        image: smtc_where_indexing
        environment:
            INDEXES: "recordings,analytics"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://defn(`OFFICE_NAME')_db:9200"
            SERVICE_INTERVAL: "30"
            UPDATE_INTERVAL: "5"
            SEARCH_BATCH: "3000"
            UPDATE_BATCH: "500"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro

    defn(`OFFICE_NAME')_analytics:
        image: `smtc_analytics_object_detection_'translit(defn(`PLATFORM'),'A-Z','a-z'):latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://defn(`OFFICE_NAME')_db:9200"
            MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            STHOST: "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            EVERY_NTH_FRAME: "6"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - defn(`OFFICE_NAME')_andata:/home/video-analytics/app/server/recordings:rw
            - /etc/localtime:/etc/localtime:ro
        deploy:
            replicas: defn(`NANALYTICS')

    defn(`OFFICE_NAME')_mqtt:
        image: eclipse-mosquitto:1.5.8
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro

    defn(`OFFICE_NAME')_storage:
        image: smtc_storage_manager:latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://defn(`OFFICE_NAME')_db:9200"
            INDEXES: "recordings,analytics"
            RECORDING_INDEX: "recordings"
            SENSOR_INDEX: "sensors"
            RETENTION_TIME: "7200"
            SERVICE_INTERVAL: "7200"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
            - defn(`OFFICE_NAME')_stdata:/var/www:rw
