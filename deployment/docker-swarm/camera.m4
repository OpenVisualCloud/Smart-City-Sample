
    defn(`OFFICE_NAME')_simulated_cameras:
        image: smtc_sensor_simulation:latest
        environment:
ifelse(defn(`SCENARIO_NAME'),`traffic',`dnl
            FILES: "traffic.mp4$$"
')dnl
ifelse(defn(`SCENARIO_NAME'),`stadium',`dnl
            FILES: "people.mp4$$"
')dnl
            `NCAMERAS': "defn(`NCAMERAS')"
            RTSP_PORT: "defn(`CAMERA_RTSP_PORT')"
            RTP_PORT: "defn(`CAMERA_RTP_PORT')"
            PORT_STEP: "defn(`CAMERA_PORT_STEP')"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet

ifelse(defn(`SCENARIO_NAME'),`stadium',`
    defn(`OFFICE_NAME')_simulated_cameras_crowd:
        image: smtc_sensor_simulation:latest
        environment:
            FILES: "crowd.mp4$$"
            `NCAMERAS': "defn(`NCAMERAS2')"
            RTSP_PORT: "defn(`CAMERA_RTSP_PORT')"
            RTP_PORT: "defn(`CAMERA_RTP_PORT')"
            PORT_STEP: "defn(`CAMERA_PORT_STEP')"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
                    
    defn(`OFFICE_NAME')_simulated_cameras_queue:
        image: smtc_sensor_simulation:latest
        environment:
            FILES: "queue.mp4$$"
            `NCAMERAS': "defn(`NCAMERAS3')"
            RTSP_PORT: "defn(`CAMERA_RTSP_PORT')"
            RTP_PORT: "defn(`CAMERA_RTP_PORT')"
            PORT_STEP: "defn(`CAMERA_PORT_STEP')"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
')
