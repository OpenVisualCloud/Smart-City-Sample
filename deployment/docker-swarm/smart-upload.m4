
    defn(`OFFICE_NAME')_smart_upload:
        image: defn(`REGISTRY_PREFIX')smtc_smart_upload:latest
        environment:
            QUERY: "objects.detection.bounding_box.x_max-objects.detection.bounding_box.x_min>0.1"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')_db):9200"
            DBCHOST: "http://cloud_gateway:8080/cloud/api/db"
            STHOST: "http://defn(`OFFICE_NAME')_storage:8080/recording"
            STCHOST: "http://cloud_gateway:8080/cloud/api/upload"
            SERVICE_INTERVAL: "30"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        deploy:
            resources:
                limits:
                    cpus: '0.05'
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes


