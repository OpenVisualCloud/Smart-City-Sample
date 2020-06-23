include(office.m4)
include(platform.m4)

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
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-smart-upload
          image: smtc_smart_upload:latest
          imagePullPolicy: IfNotPresent
          resources:
            limits:
                cpu: "50m"
          env:
            - name: QUERY
              value: "objects.detection.bounding_box.x_max-objects.detection.bounding_box.x_min>0.1"
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: STHOSTL
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/recording"
            - name: STHOSTC
              value: "http://cloud-storage-service:8080/api/upload"
            - name: SERVICE_INTERVAL
              value: "30"
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
