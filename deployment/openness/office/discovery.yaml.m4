include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

ifelse(defn(`DISCOVER_SIMULATED_CAMERA'),`true',`
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
              value: "-p T:defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS')*defn(`CAMERA_PORT_STEP')) defn(`CAMERA_HOST') -Pn"
            - name: SIM_PORT
              value: "loop(`CAMERAIDX',1,defn(`NCAMERAS'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))/')"
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
PLATFORM_NODE_SELECTOR(`Xeon')dnl

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
              value: "loop(`CAMERAIDX',1,defn(`NCAMERAS2'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))/')"
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
PLATFORM_NODE_SELECTOR(`Xeon')dnl

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-camera-discovery-entrance
  labels:
     app: defn(`OFFICE_NAME')-camera-discovery-entrance
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-camera-discovery-entrance
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-camera-discovery-entrance
    spec:
      containers:
        - name: defn(`OFFICE_NAME')-camera-discovery-entrance
          image: smtc_onvif_discovery:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: PORT_SCAN
              value: "-p T:defn(`CAMERA_RTSP_PORT')-eval(defn(`CAMERA_RTSP_PORT')+defn(`NCAMERAS3')*defn(`CAMERA_PORT_STEP')) defn(`OFFICE_NAME')-cameras-entrance-service -Pn"
            - name: SIM_PORT
              value: ifelse(eval(defn(`NCAMERAS3')>0),1,"loop(`CAMERAIDX',1,defn(`NCAMERAS3'),`eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))/')","0")
            - name: SIM_PREFIX
              value: "`cams'defn(`SCENARIOIDX')`o'defn(`OFFICEIDX')q"
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
PLATFORM_NODE_SELECTOR(`Xeon')dnl
')')

ifelse(defn(`DISCOVER_IP_CAMERA'),`true',`dnl
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-ipcamera-discovery
  labels:
     app: defn(`OFFICE_NAME')-ipcamera-discovery
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-ipcamera-discovery
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-ipcamera-discovery
    spec:
      enableServiceLinks: false
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
      containers:
        - name: defn(`OFFICE_NAME')-ipcamera-discovery
          image: smtc_onvif_discovery:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: PORT_SCAN
              value: "-p T:80-65535 defn(`IP_CAMERA_NETWORK')"
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
PLATFORM_NODE_SELECTOR(`Xeon')dnl
')

---
')')')

