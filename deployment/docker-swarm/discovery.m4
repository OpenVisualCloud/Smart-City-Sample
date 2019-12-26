
ifelse(defn(`DISCOVER_SIMULATED_CAMERA'),`true',`dnl

    defn(`OFFICE_NAME')_camera_discovery:
        image: smtc_onvif_discovery:latest
        environment:
            PORT_SCAN: "-p T:defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS')*defn(`CAMERA_PORT_STEP')) defn(`OFFICE_NAME')_simulated_cameras"
            SIM_PORT: "forloop(`CAMERAIDX',1,defn(`NCAMERAS'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))/')"
            SIM_PREFIX: "`cams'defn(`SCENARIOIDX')`o'defn(`OFFICEIDX')c"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            SERVICE_INTERVAL: "30"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet

ifelse(defn(`SCENARIO_NAME'),`stadium',`
    defn(`OFFICE_NAME')_camera_discovery_crowd:
        image: smtc_onvif_discovery:latest
        environment:
            PORT_SCAN: "-p T:defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS2')*defn(`CAMERA_PORT_STEP')) defn(`OFFICE_NAME')_simulated_cameras_crowd"
            SIM_PORT: "forloop(`CAMERAIDX',1,defn(`NCAMERAS2'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))/')"
            SIM_PREFIX: "`cams'defn(`SCENARIOIDX')`o'defn(`OFFICEIDX')w"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            SERVICE_INTERVAL: "30"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
')dnl

    defn(`OFFICE_NAME')_camera_discovery_queue:
        image: smtc_onvif_discovery:latest
        environment:
            PORT_SCAN: "-p T:defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS3')*defn(`CAMERA_PORT_STEP')) defn(`OFFICE_NAME')_simulated_cameras_queue"
            SIM_PORT: "forloop(`CAMERAIDX',1,defn(`NCAMERAS3'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))/')"
            SIM_PREFIX: "`cams'defn(`SCENARIOIDX')`o'defn(`OFFICEIDX')q"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            SERVICE_INTERVAL: "30"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
')dnl

ifelse(defn(`DISCOVER_IP_CAMERA'),`true',`dnl

    defn(`OFFICE_NAME')_ipcamera_discovery:
        image: smtc_onvif_discovery:latest
        environment:
            PORT_SCAN: "-p T:80-65535 defn(`IP_CAMERA_NETWORK')"
            OFFICE: "defn(`OFFICE_LOCATION')"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,db):9200"
            SERVICE_INTERVAL: "30"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
')dnl
