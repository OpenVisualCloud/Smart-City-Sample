
    cloud_storage:
        image: smtc_storage_manager:latest
        environment:
            DBHOST: "http://cloud_db:9200"
            INDEXES: "recordings_c,analytics"
            RECORDING_INDEX: "recordings"
            RETENTION_TIME: "7200"
            SERVICE_INTERVAL: "7200"
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
                    - node.role==manager

