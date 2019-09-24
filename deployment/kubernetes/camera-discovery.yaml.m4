# OFFICEIDX
include(office.m4)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-camera-discovery
  labels:
     app: defn(`OFFICE_NAME')-camera-discovery
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-camera-discovery
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-camera-discovery
    spec:
      containers:
        - name: defn(`OFFICE_NAME')-camera-discovery
          image: smtc_onvif_discovery:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: IP_SCAN_RANGE
              value: "defn(`OFFICE_NAME')-cameras-service"
            - name: PORT_SCAN_RANGE
              value: "defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS')*defn(`CAMERA_PORT_STEP'))"
            - name: SIMULATED_CAMERA
              value: "forloop(`cid',1,defn(`NCAMERAS'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`cid')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP')),')"
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: LOCATION
              value: "forloop(`cid',1,defn(`NCAMERAS'),`defn(`location_'defn(`OFFICE_NAME')`_camera'defn(`cid')) ')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
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
