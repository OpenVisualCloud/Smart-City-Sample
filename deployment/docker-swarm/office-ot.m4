
ifelse(defn(`OT_TYPE'),`false',,`
    defn(`OFFICE_NAME')_object_tracking:
        image: defn(`REGISTRY_PREFIX')smtc_object_tracking:latest
        volumes:
            - /etc/localtime:/etc/localtime:ro
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')_db):9200"
            MQTT_TOPIC: "relayanalytics"
            MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            `SCENARIO': "defn(`SCENARIO_NAME')"
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
')
