ifelse(eval(defn(`NOFFICES')>1),1,`

    defn(`OFFICE_NAME')_db:
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
        environment:
            - "cluster.name=db-cluster"
            - "node.name=defn(`OFFICE_NAME')_db"
            - "node.master=false"
            - "node.data=true"
            - "discovery.zen.minimum_master_nodes=1"
            - "discovery.zen.ping.unicast.hosts=cloud_db"
            - "action.auto_create_index=0"
            - "ES_JAVA_OPTS=-Xms4096m -Xmx4096m"
            - "NO_PROXY=*"
            - "no_proxy=*"
        networks:
            - db_net
        deploy:
            placement:
                constraints: [node.labels.defn(`OFFICE_NAME')_zone==yes]
')

    defn(`OFFICE_NAME')_db_init:
        image: smtc_db_init:latest
        environment:
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            OFFICE: "defn(`OFFICE_LOCATION')"
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - db_net
        deploy:
            restart_policy:
                condition: none
            placement:
                constraints: [ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)]

    defn(`OFFICE_NAME')_webproxy:
        image: smtc_web_local:latest
        environment:
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            OFFICE: "defn(`OFFICE_LOCATION')"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - ${STORAGE_VOLUME}:/mnt/storage:ro
            - /etc/localtime:/etc/localtime:ro
        networks:
            - db_net
            - defn(`OFFICE_NAME')_net
        deploy:
            placement:
                constraints: ifelse(eval(defn(`NOFFICES')>1),1,`
                    - node.labels.defn(`OFFICE_NAME')_zone==yes
                    - node.labels.defn(`OFFICE_NAME')_storage==yes
',`[node.role==manager]')

    defn(`OFFICE_NAME')_cleanup:
        image: smtc_storage_cleanup:latest
        volumes:
            - ${STORAGE_VOLUME}:/mnt/storage:rw
        environment:
            INDEXES: "recordings,analytics"
            RETENTION_TIME: "14400"
            SERVICE_INTERVAL: "14400"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - db_net
            - defn(`OFFICE_NAME')_net
        deploy:
            placement:
                constraints: ifelse(eval(defn(`NOFFICES')>1),1,`
                    - node.labels.defn(`OFFICE_NAME')_zone==yes
                    - node.labels.defn(`OFFICE_NAME')_storage==yes
',`[node.role==manager]')

    defn(`OFFICE_NAME')_camera_discovery:
        image: smtc_onvif_discovery:latest
        environment:
            IP_SCAN_RANGE: "defn(`CAMERA_NETWORK')"
            PORT_SCAN_RANGE: "0-65535"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DISTANCE: "10"
            ANGLEOFFSET: "15"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - db_net
            - defn(`OFFICE_NAME')_net
        deploy:
            placement:
                constraints: [ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)]

    defn(`OFFICE_NAME')_health_check:
        image: smtc_trigger_health
        volumes:
            - /etc/localtime:/etc/localtime:ro
        environment:
            SERVICE_INTERVAL: "300"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - db_net
            - defn(`OFFICE_NAME')_net
        deploy:
            placement:
                constraints: [ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)]

    defn(`OFFICE_NAME')_where_indexing:
        image: smtc_where_indexing
        environment:
            INDEXES: "recordings,analytics"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            SERVICE_INTERVAL: "30"
            UPDATE_INTERVAL: "5"
            SEARCH_BATCH: "3000"
            UPDATE_BATCH: "500"
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - db_net
            - defn(`OFFICE_NAME')_net
        deploy:
            placement:
                constraints: [ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)]

    defn(`OFFICE_NAME')_analytics:
        image: `smtc_analytics_object_detection_'translit(defn(`PLATFORM'),'A-Z','a-z'):latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            EVERY_NTH_FRAME: "6"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - ${STORAGE_VOLUME}:/home/video-analytics/app/server/recordings:rw
            - /etc/localtime:/etc/localtime:ro
        networks:
            - db_net
            - patsubst(defn(`OFFICE_NAME'),`office',`camera')_net
            - defn(`OFFICE_NAME')_net
        deploy:
            replicas: defn(`NSERVICES')
            placement:
                constraints: ifelse(eval(defn(`NOFFICES')>1),1,`
                    - node.labels.defn(`OFFICE_NAME')_zone==yes
                    - node.labels.defn(`OFFICE_NAME')_storage==yes
',`[node.role==manager]')

    defn(`OFFICE_NAME')_mqtt:
        image: eclipse-mosquitto:1.5.8
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - defn(`OFFICE_NAME')_net
        deploy:
            placement:
                constraints: [ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)]

