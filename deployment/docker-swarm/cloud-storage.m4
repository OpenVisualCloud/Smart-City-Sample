
    cloud_storage:
        image: smtc_storage_manager:latest
        environment:
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,cloud_db,db):9200"
            INDEXES: "recordings_c"
            PROXYHOST: "http://cloud_storage:8080"
            RETENTION_TIME: "7200"
            SERVICE_INTERVAL: "7200"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
            - cloud_stdata:/var/www:rw
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
                    - node.role==manager
