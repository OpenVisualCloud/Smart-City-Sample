include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

ifelse(defn(`DISCOVER_SIMULATED_CAMERA'),`true',`dnl

ifelse(eval(defn(`NCAMERAS')>0),1,`dnl
apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-cameras-service
  labels:
    app: defn(`OFFICE_NAME')-cameras
spec:
  ports:
loop(`CAMERAIDX',1,defn(`NCAMERAS'),`dnl
  - port: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
    protocol: TCP
    name: `rtsp'defn(`CAMERAIDX')
')dnl
  selector:
    app: defn(`OFFICE_NAME')-cameras

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-cameras
  labels:
     app: defn(`OFFICE_NAME')-cameras
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-cameras
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-cameras
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-cameras
          image: defn(`REGISTRY_PREFIX')smtc_sensor_simulation:latest
          imagePullPolicy: IfNotPresent
          ports:
loop(`CAMERAIDX',1,defn(`NCAMERAS'),`dnl
            - containerPort: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
              protocol: TCP
')dnl
          env:
ifelse(defn(`SCENARIO_NAME'),`traffic',`dnl
            - name: FILES
              value: "_traffic.mp4$$"
            - name: ALGORITHM
              value: "object-detection"
')dnl
ifelse(defn(`SCENARIO_NAME'),`stadium',`dnl
            - name: FILES
              value: "_svcq.mp4$$"
            - name: ALGORITHM
              value: "svcq-counting"
')dnl
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: `NCAMERAS'
              value: "defn(`NCAMERAS')"
            - name: RTSP_PORT
              value: "defn(`CAMERA_RTSP_PORT')"
            - name: RTP_PORT
              value: "defn(`CAMERA_RTP_PORT')"
            - name: PORT_STEP
              value: "defn(`CAMERA_PORT_STEP')"
PLATFORM_NODE_SELECTOR(`Xeon')dnl
')dnl

ifelse(defn(`SCENARIO_NAME'),`stadium',`dnl
---

ifelse(eval(defn(`NCAMERAS2')>0),1,`dnl
apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-cameras-crowd-service
  labels:
    app: defn(`OFFICE_NAME')-cameras-crowd
spec:
  ports:
loop(`CAMERAIDX',1,defn(`NCAMERAS2'),`dnl
  - port: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
    protocol: TCP
    name: `rtsp'defn(`CAMERAIDX')
')dnl
  selector:
    app: defn(`OFFICE_NAME')-cameras-crowd

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-cameras-crowd
  labels:
     app: defn(`OFFICE_NAME')-cameras-crowd
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-cameras-crowd
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-cameras-crowd
    spec:
      containers:
        - name: defn(`OFFICE_NAME')-cameras-crowd
          image: defn(`REGISTRY_PREFIX')smtc_sensor_simulation:latest
          imagePullPolicy: IfNotPresent
          ports:
loop(`CAMERAIDX',1,defn(`NCAMERAS2'),`dnl
            - containerPort: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
              protocol: TCP
')dnl
          env:
            - name: FILES
              value: "_crowd.mp4$$"
            - name: ALGORITHM
              value: "crowd-counting"
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: `NCAMERAS'
              value: "defn(`NCAMERAS2')"
            - name: RTSP_PORT
              value: "defn(`CAMERA_RTSP_PORT')"
            - name: RTP_PORT
              value: "defn(`CAMERA_RTP_PORT')"
            - name: PORT_STEP
              value: "defn(`CAMERA_PORT_STEP')"
PLATFORM_NODE_SELECTOR(`Xeon')dnl
')dnl

---

ifelse(eval(defn(`NCAMERAS3')>0),1,`dnl
apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-cameras-entrance-service
  labels:
    app: defn(`OFFICE_NAME')-cameras-entrance
spec:
  ports:
loop(`CAMERAIDX',1,defn(`NCAMERAS3'),`dnl
  - port: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
    protocol: TCP
    name: `rtsp'defn(`CAMERAIDX')
')dnl
  selector:
    app: defn(`OFFICE_NAME')-cameras-entrance

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-cameras-entrance
  labels:
     app: defn(`OFFICE_NAME')-cameras-entrance
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-cameras-entrance
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-cameras-entrance
    spec:
      containers:
        - name: defn(`OFFICE_NAME')-cameras-entrance
          image: defn(`REGISTRY_PREFIX')smtc_sensor_simulation:latest
          imagePullPolicy: IfNotPresent
          ports:
loop(`CAMERAIDX',1,defn(`NCAMERAS3'),`dnl
            - containerPort: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
              protocol: TCP
')dnl
          env:
            - name: FILES
              value: "_entrance.mp4$$"
            - name: ALGORITHM
              value: "entrance-counting"
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: `NCAMERAS'
              value: "defn(`NCAMERAS3')"
            - name: RTSP_PORT
              value: "defn(`CAMERA_RTSP_PORT')"
            - name: RTP_PORT
              value: "defn(`CAMERA_RTP_PORT')"
            - name: PORT_STEP
              value: "defn(`CAMERA_PORT_STEP')"
PLATFORM_NODE_SELECTOR(`Xeon')dnl
')dnl
')dnl
')dnl

---
')')')
