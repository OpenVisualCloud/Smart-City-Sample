
    defn(`OFFICE_NAME')_camera_discovery:
        image: smtc_onvif_discovery:latest
        environment:
            IP_SCAN_RANGE: "defn(`OFFICE_NAME')_simulated_cameras"
            PORT_SCAN_RANGE: "defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS')*defn(`CAMERA_PORT_STEP'))"
            SIMULATED_CAMERA: "forloop(`cid',1,defn(`NCAMERAS'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`cid')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP')),')"
            OFFICE: "defn(`OFFICE_LOCATION')"
            LOCATION: "forloop(`cid',1,defn(`NCAMERAS'),`defn(`location_'defn(`OFFICE_NAME')`_camera'defn(`cid')) ')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            SERVICE_INTERVAL: "30"
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
