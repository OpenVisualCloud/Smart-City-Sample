
    cloud_storage:
        image: defn(`REGISTRY_PREFIX')smtc_storage_manager:latest
        environment:
            DBHOST: "http://ifelse(defn(`NOFFICES'),1,db,cloud_db):9200"
            INDEXES: "recordings"
            RETENTION_TIME: "7200"
            SERVICE_INTERVAL: "3600"
            WARN_DISK: "70"
            FATAL_DISK: "75"
            HALT_REC: "80"
            THUMBNAIL_CACHE: "50"
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
