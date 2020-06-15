define(`SERVICE_INTERVAL_SMART_UPLOAD',`120')dnl

    defn(`OFFICE_NAME')_smart_upload:
        image: defn(`REGISTRY_PREFIX')smtc_smart_upload:latest
        environment:
            QUERY: "uploaded=false"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            STHOSTL: "http://defn(`OFFICE_NAME')_storage:8080/recording"
            STHOSTC: "http://cloud_storage:8080/api/upload"
            SERVICE_INTERVAL: defn(`SERVICE_INTERVAL_SMART_UPLOAD')
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        deploy:
            resources:
                limits:
                    cpus: '0.20'
                reservations:
                    cpus: '0.10'
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes


