
    defn(`OFFICE_NAME')_gateway:
        image: defn(`REGISTRY_PREFIX')smtc_api_gateway:latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')_db):9200"
            STHOST: "http://defn(`OFFICE_NAME')_storage:8080"
            WEBRTCHOST: "http://defn(`OFFICE_NAME')_webrtc:8888"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
