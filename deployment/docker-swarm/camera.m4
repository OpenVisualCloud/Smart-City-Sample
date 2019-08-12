    defn(`OFFICE_NAME')_simulated_cameras:
        image: smtc_sensor_simulation:latest
        environment:
            OFFICE: 'defn(`OFFICE_LOCATION')'
            DISTANCE: '20'
            SENSORS: '3'
            SENSOR_ID: '{{.Task.Slot}}'
            DBHOST: 'http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200'
            FILES: '.mp4$$'
            THETA: 105
            MNTH: 15.0
            ALPHA: 45
            FOVH: 90
            FOVV: 68
            NO_PROXY: '*'
            no_proxy: '*'
        networks:
            - db_net
            - defn(`OFFICE_NAME')_net
            - defn(`OFFICE_NAME')_camera_net
        deploy:
            replicas: 3
            placement:
                constraints: ifelse(eval(defn(`NOFFICES')>1),1,[node.labels.zone==defn(`OFFICE_NAME')],[node.role==manager])
