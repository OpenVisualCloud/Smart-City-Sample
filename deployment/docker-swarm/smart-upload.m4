define(`SERVICE_INTERVAL_SMART_UPLOAD',`120')dnl

    defn(`OFFICE_NAME')_smart_upload:
        image: smtc_smart_upload:latest
        environment:
            QUERY: "time>=now-eval(defn(`SERVICE_INTERVAL_SMART_UPLOAD')*1000) where objects.detection.bounding_box.x_max-objects.detection.bounding_box.x_min>0.01"
            INDEXES: "recordings,analytics"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            SMHOST: "http://defn(`OFFICE_NAME')_storage:8080/recording"
            CLOUDHOST: "http://cloud_storage:8080/recording"
            SERVICE_INTERVAL: defn(`SERVICE_INTERVAL_SMART_UPLOAD')
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
                    - defn(`OFFICE_ZONE')
            resources:
                limits:
                    cpus: '0.20'
                reservations:
                    cpus: '0.10'

