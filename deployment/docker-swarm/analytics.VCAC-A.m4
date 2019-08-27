    defn(`OFFICE_NAME')_analytics:
        image: docker
        command: "docker run --env OFFICE='defn(`OFFICE_LOCATION')' --env DBHOST='http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200' --env MQTTHOST='defn(`OFFICE_NAME')_mqtt' --env EVERY_NTH_FRAME=6 --env NO_PROXY='*' --env no_proxy='*' --user root -v /tmp:/tmp -v /var/tmp:/var/tmp -v /etc/localtime:/etc/localtime:ro -v /mnt/storage:/home/video-analytics/app/server/recordings:rw --device=/dev/ion:/dev/ion --privileged --network patsubst(defn(`OFFICE_NAME'),`office',`smtc_office')_net smtc_analytics_object_detection_vcac-a:latest"
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
        deploy:
            replicas: defn(`NSERVICES')
            placement:
                constraints:
                    - node.labels.defn(`OFFICE_NAME')_vcac_zone==yes
                    - node.labels.defn(`OFFICE_NAME')_vcac_storage==yes
