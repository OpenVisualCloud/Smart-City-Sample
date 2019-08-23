forloop(`camera_idx',`1',`5',`dnl
define(`CAMERA_NAME',`camera'defn(`camera_idx'))dnl
define(`CAMERA_LOCATION_NAME',`location_'defn(`OFFICE_NAME')`_'defn(`CAMERA_NAME'))dnl
ifdef(defn(`CAMERA_LOCATION_NAME'),`dnl
    defn(`OFFICE_NAME')`_simulated_'defn(`CAMERA_NAME'):
        image: smtc_sensor_simulation:latest
        environment:
            OFFICE: "defn(`OFFICE_LOCATION')"
            SENSOR_ID: "defn(`camera_idx')"
            LOCATION: "defn(defn(`CAMERA_LOCATION_NAME'))"
            DBHOST: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')_db,cloud_db):9200"
            FILES: ".mp4$$"
            THETA: 105
            MNTH: 15.0
            ALPHA: 45
            FOVH: 90
            FOVV: 68
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - db_net
            - patsubst(defn(`OFFICE_NAME'),`office',`camera')_net
        deploy:
            placement:
                constraints: [ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)]

')dnl
')dnl
