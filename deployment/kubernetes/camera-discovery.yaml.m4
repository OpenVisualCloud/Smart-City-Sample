include(office.m4)
include(../../script/forloop.m4)

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
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-camera-discovery
          image: smtc_onvif_discovery:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: PORT_SCAN
              value: "-p T:defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS')*defn(`CAMERA_PORT_STEP')) defn(`OFFICE_NAME')-cameras-service -Pn"
            - name: SIM_PORT
              value: "forloop(`CAMERAIDX',1,defn(`NCAMERAS'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))/')"
            - name: SIM_PREFIX
              value: "`cams'defn(`SCENARIOIDX')`o'defn(`OFFICEIDX')c"
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
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
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-ipcamera-discovery
  labels:
     app: defn(`OFFICE_NAME')-ipcamera-discovery
spec:
  replicas: 0
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-ipcamera-discovery
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-ipcamera-discovery
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-ipcamera-discovery
          image: smtc_onvif_discovery:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: PORT_SCAN
              value: "-p T:80-65535 192.168.defn(`OFFICEIDX').0/24"
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
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
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl

ifelse(defn(`SCENARIO_NAME'),`stadium',`
---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-camera-discovery-crowd
  labels:
     app: defn(`OFFICE_NAME')-camera-discovery-crowd
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-camera-discovery-crowd
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-camera-discovery-crowd
    spec:
      containers:
        - name: defn(`OFFICE_NAME')-camera-discovery-crowd
          image: smtc_onvif_discovery:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: PORT_SCAN
              value: "-p T:defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS2')*defn(`CAMERA_PORT_STEP')) defn(`OFFICE_NAME')-cameras-crowd-service -Pn"
            - name: SIM_PORT
              value: "forloop(`CAMERAIDX',1,defn(`NCAMERAS2'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))/')"
            - name: SIM_PREFIX
              value: "`cams'defn(`SCENARIOIDX')`o'defn(`OFFICEIDX')w"
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
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
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl
')dnl
