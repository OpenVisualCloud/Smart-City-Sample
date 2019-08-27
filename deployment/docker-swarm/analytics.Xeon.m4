    defn(`OFFICE_NAME')_analytics:
        image: `smtc_analytics_object_detection_'translit(defn(`PLATFORM'),'A-Z','a-z'):latest
        environment:
            OFFICE: 'defn(`OFFICE_LOCATION')'
            DBHOST: 'http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200'
            MQTTHOST: 'defn(`OFFICE_NAME')_mqtt'
            EVERY_NTH_FRAME: 6
            NO_PROXY: '*'
            no_proxy: '*'
        volumes:
            - ${STORAGE_VOLUME}:/home/video-analytics/app/server/recordings:rw
            - /etc/localtime:/etc/localtime:ro
        deploy:
            replicas: defn(`NSERVICES')
            placement:
                constraints: ifelse(eval(defn(`NOFFICES')>1),1,`
                    - node.labels.defn(`OFFICE_NAME')_zone==yes
                    - node.labels.defn(`OFFICE_NAME')_storage==yes
',`[node.role==manager]')

