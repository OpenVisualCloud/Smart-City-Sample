
    cloud_where_indexing:
        image: defn(`REGISTRY_PREFIX')smtc_where_indexing:latest
        environment:
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,cloud_db,db):9200"
            SERVICE_INTERVAL: "30"
            UPDATE_INTERVAL: "5"
            SEARCH_BATCH: "3000"
            UPDATE_BATCH: "500"
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

