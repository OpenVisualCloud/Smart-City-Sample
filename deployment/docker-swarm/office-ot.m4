
ifelse(defn(`OT_TYPE'),`false',,`
    defn(`OFFICE_NAME')_object_tracking:
        image: IMAGENAME(smtc_object_tracking)
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
        secrets:
            - source: self_crt
              target: self.crt
              uid: "defn(`USER_ID')"
              gid: "defn(`GROUP_ID')"
              mode: 0444
            - source: mqtt-defn(`OFFICEIDX')-client-key
              target: mqtt_client.key
              uid: "defn(`USER_ID')"
              gid: "defn(`GROUP_ID')"
              mode: 0440
            - source: mqtt-defn(`OFFICEIDX')-client-crt
              target: mqtt_client.crt
              uid: "defn(`USER_ID')"
              gid: "defn(`GROUP_ID')"
              mode: 0440
        networks:
            - appnet
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
')
