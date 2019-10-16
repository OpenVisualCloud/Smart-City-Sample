
ifelse(defn(`SCENARIO_NAME'),`traffic',`
    defn(`OFFICE_NAME')_analytics:
        image: vcac-container-launcher:latest
        command: ["--volume","defn(`OFFICE_NAME')_andata:/home/video-analytics/app/server/recordings:rw","--network","smtc_default_net",`"smtc_analytics_object_detection_vcac-a_'defn(`FRAMEWORK'):latest"]
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - defn(`OFFICE_NAME')_andata:/home/video-analytics/app/server/recordings:rw
            - /etc/localtime:/etc/localtime:ro
        environment:
            VCAC_OFFICE: "defn(`OFFICE_LOCATION')"
            VCAC_DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            VCAC_MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            VCAC_EVERY_NTH_FRAME: 6
            VCAC_STHOST: "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            VCAC_NO_PROXY: "*"
            VCAC_no_proxy: "*"
        networks:
            - default_net
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - node.labels.vcac_zone==yes
')
