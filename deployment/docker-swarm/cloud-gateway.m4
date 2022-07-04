
    cloud_gateway:
        image: IMAGENAME(smtc_api_gateway)
        environment:
            DBHOST: "http://ifelse(defn(`NOFFICES'),1,db,cloud_db):9200"
            STHOST: "http://cloud_storage:8080"
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
