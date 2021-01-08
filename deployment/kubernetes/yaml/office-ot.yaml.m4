include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)

ifelse(len(defn(`OFFICE_LOCATION')),0,,`
ifelse(defn(`OT_TYPE'),`false',,`dnl

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-object-tracking
  labels:
     app: defn(`OFFICE_NAME')-object-tracking
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-object-tracking
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-object-tracking
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-object-tracking
          image: defn(`REGISTRY_PREFIX')smtc_object_tracking:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: MQTT_TOPIC
              value: "relayanalytics"
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
')dnl
')')')
