include(office.m4)
define(`SERVICE_INTERVAL_SMART_UPLOAD',120)dnl

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-smart-upload
  labels:
     app: defn(`OFFICE_NAME')-smart-upload
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-smart-upload
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-smart-upload
    spec:
      containers:
        - name: defn(`OFFICE_NAME')-smart-upload
          image: smtc_smart_upload:latest
          imagePullPolicy: IfNotPresent
          resources:
            requests:
                cpu: "100m"
            limits:
                cpu: "200m"
          env:
            - name: QUERY
              value: "time>=eval(defn(`SERVICE_INTERVAL_SMART_UPLOAD')*1000) where objects.detection.bounding_box.x_max-objects.detection.bounding_box.x_min>0.01"
            - name: INDEXES
              value: "recordings,analytics"
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: SMHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/recording"
            - name: CLOUDHOST
              value: "http://cloud-storage-service:8080/recording"
            - name: SERVICE_INTERVAL
              value: "defn(`SERVICE_INTERVAL_SMART_UPLOAD')"
            - name: UPDATE_INTERVAL
              value: "5"
            - name: SEARCH_BATCH
              value: "3000"
            - name: UPDATE_BATCH
              value: "500"
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

