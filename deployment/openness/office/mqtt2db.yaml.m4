include(office.m4)
include(platform.m4)

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
          image: smtc_mqtt2db:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: `SCENARIO'
              value: "defn(`SCENARIO')"
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
