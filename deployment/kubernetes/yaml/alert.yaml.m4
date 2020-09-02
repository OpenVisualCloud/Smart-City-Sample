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
  name: defn(`OFFICE_NAME')-alert
  labels:
     app: defn(`OFFICE_NAME')-alert
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-alert
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-alert
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-alert
          image: defn(`REGISTRY_PREFIX')smtc_alert:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: SERVICE_INTERVAL
              value: "3,5,15"
            - name: OCCUPENCY_ARGS
              value: "100000,8,3,1000,20"
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
