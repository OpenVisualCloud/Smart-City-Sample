
    defn(`OFFICE_NAME')_where_indexing:
        image: smtc_where_indexing:latest
        environment:
            INDEXES: "recordings,analytics"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            SERVICE_INTERVAL: "30"
            UPDATE_INTERVAL: "5"
            SEARCH_BATCH: "3000"
            UPDATE_BATCH: "500"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
                    - ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)

