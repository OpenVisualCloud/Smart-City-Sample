
    defn(`OFFICE_NAME')_simulated_cameras:
        image: smtc_sensor_simulation:latest
        environment:
            FILES: ".mp4$$"
            `NCAMERAS': "defn(`NCAMERAS')"
            RTSP_PORT: "defn(`CAMERA_RTSP_PORT')"
            RTP_PORT: "defn(`CAMERA_RTP_PORT')"
            PORT_STEP: "defn(`CAMERA_PORT_STEP')"
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
