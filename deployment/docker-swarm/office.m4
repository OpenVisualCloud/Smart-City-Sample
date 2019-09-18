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
        volumes:
            - /etc/localtime:/etc/localtime:ro
            - defn(`OFFICE_NAME')_esdata:/usr/share/elasticsearch/data:rw
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
                    - node.labels.defn(`OFFICE_NAME')_zone==yes

')

    defn(`OFFICE_NAME')_db_init:
        image: smtc_db_init:latest
        environment:
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            OFFICE: "defn(`OFFICE_LOCATION')"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            restart_policy:
                condition: none
            placement:
                constraints:
                    - ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)

    defn(`OFFICE_NAME')_camera_discovery:
        image: smtc_onvif_discovery:latest
        environment:
            IP_SCAN_RANGE: "defn(`OFFICE_NAME')_simulated_cameras"
            PORT_SCAN_RANGE: "defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS')*defn(`CAMERA_PORT_STEP'))"
            SIMULATED_CAMERA: "forloop(`cid',1,defn(`NCAMERAS'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`cid')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP')),')"
            OFFICE: "defn(`OFFICE_LOCATION')"
            LOCATION: "forloop(`cid',1,defn(`NCAMERAS'),`defn(`location_'defn(`OFFICE_NAME')`_camera'defn(`cid')) ')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            SERVICE_INTERVAL: "30"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
                    - ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)

    defn(`OFFICE_NAME')_health_check:
        image: smtc_trigger_health:latest
        volumes:
            - /etc/localtime:/etc/localtime:ro
        environment:
            SERVICE_INTERVAL: "300"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            NO_PROXY: "*"
            no_proxy: "*"
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
                    - ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)

    defn(`OFFICE_NAME')_where_indexing:
        image: smtc_where_indexing:latest
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
        volumes:
            - /etc/localtime:/etc/localtime:ro
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
                    - ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)

    defn(`OFFICE_NAME')_smart_upload:
        image: smtc_smart_upload:latest
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
        volumes:
            - /etc/localtime:/etc/localtime:ro
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            restart_policy:
                condition: none
            placement:
                constraints:
                    - ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)

    defn(`OFFICE_NAME')_storage:
        image: smtc_storage_manager:latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            INDEXES: "recordings,analytics"
            RETENTION_TIME: "14400"
            SERVICE_INTERVAL: "14400"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
            - defn(`OFFICE_NAME')_stdata:/var/www:rw
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
                    - node.labels.defn(`OFFICE_NAME')_zone==yes
                    - node.labels.defn(`OFFICE_NAME')_storage==yes
',`dnl
                    - node.role==manager
')dnl

    defn(`OFFICE_NAME')_mqtt:
        image: eclipse-mosquitto:1.5.8
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
                    - ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)

