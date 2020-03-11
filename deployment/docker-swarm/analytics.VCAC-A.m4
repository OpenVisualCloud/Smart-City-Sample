
ifelse(defn(`SCENARIO_NAME'),`traffic',`
    defn(`OFFICE_NAME')_analytics:
        image: vcac-container-launcher:latest
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - /etc/localtime:/etc/localtime:ro
        environment:
            VCAC_IMAGE: `smtc_analytics_object_detection_vcac-a_'defn(`FRAMEWORK'):latest
            VCAC_OFFICE: "defn(`OFFICE_LOCATION')"
            VCAC_DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            VCAC_MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            VCAC_EVERY_NTH_FRAME: 6
            VCAC_SCENARIO: "defn(`SCENARIO')"
            VCAC_STHOST: "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            VCAC_PIPELINE_VERSION: 2
            VCAC_NO_PROXY: "*"
            VCAC_no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - node.labels.vcac_zone==yes
')

ifelse(defn(`SCENARIO_NAME'),`stadium',`
    defn(`OFFICE_NAME')_analytics_people:
        image: vcac-container-launcher:latest
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - /etc/localtime:/etc/localtime:ro
        environment:
            VCAC_IMAGE: `smtc_analytics_people_counting_vcac-a_'defn(`FRAMEWORK'):latest
            VCAC_OFFICE: "defn(`OFFICE_LOCATION')"
            VCAC_DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            VCAC_MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            VCAC_EVERY_NTH_FRAME: 6
            VCAC_SCENARIO: "defn(`SCENARIO')"
            VCAC_STHOST: "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            VCAC_NO_PROXY: "*"
            VCAC_no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - node.labels.vcac_zone==yes

    defn(`OFFICE_NAME')_analytics_crowd:
        image: vcac-container-launcher:latest
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - /etc/localtime:/etc/localtime:ro
        environment:
            VCAC_IMAGE: `smtc_analytics_crowd_counting_vcac-a_'defn(`FRAMEWORK'):latest
            VCAC_OFFICE: "defn(`OFFICE_LOCATION')"
            VCAC_DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            VCAC_MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            VCAC_EVERY_NTH_FRAME: 6
            VCAC_SCENARIO: "defn(`SCENARIO')"
            VCAC_STHOST: "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            VCAC_NO_PROXY: "*"
            VCAC_no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: defn(`NANALYTICS2')
            placement:
                constraints:
                    - node.labels.vcac_zone==yes

    defn(`OFFICE_NAME')_analytics_queue:
        image: vcac-container-launcher:latest
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - /etc/localtime:/etc/localtime:ro
        environment:
            VCAC_IMAGE: `smtc_analytics_object_detection_vcac-a_'defn(`FRAMEWORK'):latest
            VCAC_OFFICE: "defn(`OFFICE_LOCATION')"
            VCAC_DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            VCAC_MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            VCAC_EVERY_NTH_FRAME: 6
            VCAC_SCENARIO: "defn(`SCENARIO')"
            VCAC_STHOST: "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            VCAC_PIPELINE_VERSION: 2
            VCAC_NO_PROXY: "*"
            VCAC_no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: defn(`NANALYTICS3')
            placement:
                constraints:
                    - node.labels.vcac_zone==yes
')
