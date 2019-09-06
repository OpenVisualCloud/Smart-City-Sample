define(`CAMERA_RTSP_PORT',17000)
define(`CAMERA_RTP_PORT',27000)
define(`CAMERA_PORT_STEP',100)

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
        ifelse(defn(`PLATFORM'),`VCAC-A',`
        networks:
            - default_net')
        deploy:
            placement:
                constraints: [ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)]

