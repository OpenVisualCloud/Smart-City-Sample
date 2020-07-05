
    cloud_storage:
        image: defn(`REGISTRY_PREFIX')smtc_storage_manager:latest
        environment:
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,cloud_db,db):9200"
            INDEXES: "recordings"
            PROXYHOST: "http://cloud_storage:8080"
            RETENTION_TIME: "7200"
            SERVICE_INTERVAL: "3600"
            WARN_DISK: "75"
            FATAL_DISK: "85"
            HALT_REC: "95"
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
