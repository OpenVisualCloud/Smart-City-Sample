
    defn(`OFFICE_NAME')_simulated_cameras:
        image: defn(`REGISTRY_PREFIX')smtc_sensor_simulation:latest
        environment:
ifelse(defn(`SCENARIO_NAME'),`traffic',`dnl
            FILES: "_traffic.mp4$$"
            ALGORITHM: "object-detection"
')dnl
ifelse(defn(`SCENARIO_NAME'),`stadium',`dnl
            FILES: "_svcq.mp4$$"
            ALGORITHM: "svcq-counting"
')dnl
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            `NCAMERAS': "defn(`NCAMERAS')"
            RTSP_PORT: "defn(`CAMERA_RTSP_PORT')"
            RTP_PORT: "defn(`CAMERA_RTP_PORT')"
            PORT_STEP: "defn(`CAMERA_PORT_STEP')"
        networks:
            - appnet
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes

ifelse(defn(`SCENARIO_NAME'),`stadium',`
    defn(`OFFICE_NAME')_simulated_cameras_crowd:
        image: defn(`REGISTRY_PREFIX')smtc_sensor_simulation:latest
        environment:
            FILES: "_crowd.mp4$$"
            ALGORITHM: "crowd-counting"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            `NCAMERAS': "defn(`NCAMERAS2')"
            RTSP_PORT: "defn(`CAMERA_RTSP_PORT')"
            RTP_PORT: "defn(`CAMERA_RTP_PORT')"
            PORT_STEP: "defn(`CAMERA_PORT_STEP')"
        networks:
            - appnet
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
                    
    defn(`OFFICE_NAME')_simulated_cameras_entrance:
        image: defn(`REGISTRY_PREFIX')smtc_sensor_simulation:latest
        environment:
            FILES: "_entrance.mp4$$"
            ALGORITHM: "entrance-counting"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            `NCAMERAS': "defn(`NCAMERAS3')"
            RTSP_PORT: "defn(`CAMERA_RTSP_PORT')"
            RTP_PORT: "defn(`CAMERA_RTP_PORT')"
            PORT_STEP: "defn(`CAMERA_PORT_STEP')"
        networks:
            - appnet
        deploy:
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
')
