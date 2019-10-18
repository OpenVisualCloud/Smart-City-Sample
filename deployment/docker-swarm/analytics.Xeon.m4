
ifelse(defn(`SCENARIO_NAME'),`traffic',`
    defn(`OFFICE_NAME')_analytics:
        `image: smtc_analytics_object_detection_xeon_'defn(`FRAMEWORK'):latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            STHOST: "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            EVERY_NTH_FRAME: 6
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
            - defn(`OFFICE_NAME')_andata:/home/video-analytics/app/server/recordings:rw
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - defn(`OFFICE_ZONE')
')
ifelse(defn(`SCENARIO_NAME'),`stadium',`
    defn(`OFFICE_NAME')_analytics_people:
        `image: smtc_analytics_people_counting_xeon_'defn(`FRAMEWORK'):latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            STHOST: "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            EVERY_NTH_FRAME: 6
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - defn(`OFFICE_ZONE')

    defn(`OFFICE_NAME')_analytics_crowd:
        `image: smtc_analytics_crowd_counting_xeon_'defn(`FRAMEWORK'):latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            MQTTHOST: "defn(`OFFICE_NAME')_mqtt"
            STHOST: "http://defn(`OFFICE_NAME')_storage:8080/api/upload"
            EVERY_NTH_FRAME: 6
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        deploy:
            replicas: defn(`NANALYTICS2')
            placement:
                constraints:
                    - defn(`OFFICE_ZONE')
')
