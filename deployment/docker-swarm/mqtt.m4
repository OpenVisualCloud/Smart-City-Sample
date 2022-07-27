
    defn(`OFFICE_NAME')_mqtt:
        image: IMAGENAME(smtc_mqttserver)
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        secrets:
            - source: self_crt
              target: self.crt
            - source: mqtt-defn(`OFFICEIDX')-server-key
              target: mqtt_server.key
            - source: mqtt-defn(`OFFICEIDX')-server-crt
              target: mqtt_server.crt
        networks:
            - appnet
        user: mosquitto
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
