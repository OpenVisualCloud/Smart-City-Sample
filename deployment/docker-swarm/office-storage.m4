
    defn(`OFFICE_NAME')_storage:
        image: IMAGENAME(smtc_storage_manager)
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')_db):9200"
            INDEXES: "recordings,analytics"
            RETENTION_TIME: "3600"
            SERVICE_INTERVAL: "1800"
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
