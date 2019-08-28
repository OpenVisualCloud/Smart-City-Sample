forloop(`camera_idx',`1',defn(`NCAMERAS'),`

define(`CAMERA_NAME',`camera'defn(`camera_idx'))
define(`CAMERA_LOCATION_NAME',`location_'defn(`OFFICE_NAME')`_'defn(`CAMERA_NAME'))

ifdef(defn(`CAMERA_LOCATION_NAME'),`

    defn(`OFFICE_NAME')`_simulated_'defn(`CAMERA_NAME'):
        image: smtc_sensor_simulation:latest
        environment:
            SENSOR_ID: "defn(`camera_idx')"
            FILES: ".mp4$$"
        deploy:
            placement:
                constraints: [ifelse(eval(defn(`NOFFICES')>1),1,node.labels.defn(`OFFICE_NAME')_zone==yes,node.role==manager)]

')
')
