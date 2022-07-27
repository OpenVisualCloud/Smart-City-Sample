
secrets:
    self_key:
        file: ../certificate/self.key
    self_crt:
        file: ../certificate/self.crt
    sensor_info:
        file: ../../maintenance/db-init/sensor-info.json

loop(`OFFICEIDX',1,defn(`NOFFICES'),`
    mqtt-defn(`OFFICEIDX')-server-key:
        file: ../certificate/swarm-defn(`OFFICEIDX')/mqtt_server.key
    mqtt-defn(`OFFICEIDX')-server-crt:
        file: ../certificate/swarm-defn(`OFFICEIDX')/mqtt_server.crt
    mqtt-defn(`OFFICEIDX')-client-key:
        file: ../certificate/swarm-defn(`OFFICEIDX')/mqtt_client.key
    mqtt-defn(`OFFICEIDX')-client-crt:
        file: ../certificate/swarm-defn(`OFFICEIDX')/mqtt_client.crt
')

