# OFFICEIDX
include(office.m4)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-health-check
  labels:
     app: defn(`OFFICE_NAME')-health-check
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-health-check
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-health-check
    spec:
      containers:
        - name: defn(`OFFICE_NAME')-health-check
          image: smtc_trigger_health:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: SERVICE_INTERVAL
              value: "300"
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
