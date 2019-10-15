include(office.m4)

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
          image: smtc_alert:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: SERVICE_INTERVAL
              value: "3,5,15"
            - name: OCCUPENCY_ARGS
              value: "120000,10,200,300"
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
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl

