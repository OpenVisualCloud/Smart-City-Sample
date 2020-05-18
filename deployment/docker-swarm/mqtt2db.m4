
    defn(`OFFICE_NAME')_mqtt2db:
        image: defn(`REGISTRY_PREFIX')smtc_mqtt2db:latest
        volumes:
            - /etc/localtime:/etc/localtime:ro
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
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
