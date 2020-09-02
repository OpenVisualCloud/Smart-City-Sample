include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-mqtt2db
  labels:
     app: defn(`OFFICE_NAME')-mqtt2db
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-mqtt2db
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-mqtt2db
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-mqtt2db
          image: defn(`REGISTRY_PREFIX')smtc_mqtt2db:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: `SCENARIO'
              value: "defn(`SCENARIO_NAME')"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
PLATFORM_NODE_SELECTOR(`Xeon')dnl

---
')')')
