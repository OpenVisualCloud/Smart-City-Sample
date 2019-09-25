# OFFICEIDX
include(office.m4)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-analytics
  labels:
     app: defn(`OFFICE_NAME')-analytics
spec:
  replicas: defn(`NANALYTICS')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-analytics
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-analytics
    spec:
      containers:
        - name: defn(`OFFICE_NAME')-analytics
          image: `smtc_analytics_object_detection_'translit(defn(`PLATFORM'),'A-Z','a-z'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/api/upload"
            - name: EVERY_NTH_FRAME
              value: "6"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /home/video-analytics/app/server/recordings
              name: defn(`OFFICE_NAME')-andata
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
          - name: defn(`OFFICE_NAME')-andata
            emptyDir: {}
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_NAME')-zone: yes
')dnl
