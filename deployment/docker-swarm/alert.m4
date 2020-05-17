
    defn(`OFFICE_NAME')_alert:
        image: defn(`DOCKER_REGISTRY')smtc_alert:latest
        volumes:
            - /etc/localtime:/etc/localtime:ro
        environment:
            SERVICE_INTERVAL: "3,5,15"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            OCCUPENCY_ARGS: "120000,8,200,300"
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
