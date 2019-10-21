include(office.m4)
include(../../script/forloop.m4)

apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-cameras-service
  labels:
    app: defn(`OFFICE_NAME')-cameras
spec:
  ports:
forloop(`CAMERAIDX',1,defn(`NCAMERAS'),`dnl
  - port: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
    protocol: TCP
    name: `rtsp'defn(`CAMERAIDX')
forloop(`STREAMIDX',1,defn(`CAMERA_PORT_STEP'),`dnl
  - port: eval(defn(`CAMERA_RTP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP')+defn(`STREAMIDX')-1)
    protocol: UDP
    name: `rtp'defn(`CAMERAIDX')`s'defn(`STREAMIDX')
')')dnl
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
          image: smtc_sensor_simulation:latest
          imagePullPolicy: IfNotPresent
          ports:
forloop(`CAMERAIDX',1,defn(`NCAMERAS'),`dnl
            - containerPort: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
              protocol: TCP
forloop(`STREAMIDX',1,defn(`CAMERA_PORT_STEP'),`dnl
            - containerPort: eval(defn(`CAMERA_RTP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP')+defn(`STREAMIDX')-1)
              protocol: UDP
')')dnl
          env:
ifelse(defn(`SCENARIO_NAME'),`traffic',`dnl
            - name: FILES
              value: "traffic.mp4$$"
')dnl
ifelse(defn(`SCENARIO_NAME'),`stadium',`dnl
            - name: FILES
              value: "people.mp4$$"
')dnl
            - name: `NCAMERAS'
              value: "defn(`NCAMERAS')"
            - name: RTSP_PORT
              value: "defn(`CAMERA_RTSP_PORT')"
            - name: RTP_PORT
              value: "defn(`CAMERA_RTP_PORT')"
            - name: PORT_STEP
              value: "defn(`CAMERA_PORT_STEP')"
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

ifelse(defn(`SCENARIO_NAME'),`stadium',`dnl
---

apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-cameras-crowd-service
  labels:
    app: defn(`OFFICE_NAME')-cameras-crowd
spec:
  ports:
forloop(`CAMERAIDX',1,defn(`NCAMERAS2'),`dnl
  - port: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
    protocol: TCP
    name: `rtsp'defn(`CAMERAIDX')
forloop(`STREAMIDX',1,defn(`CAMERA_PORT_STEP'),`dnl
  - port: eval(defn(`CAMERA_RTP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP')+defn(`STREAMIDX')-1)
    protocol: UDP
    name: `rtp'defn(`CAMERAIDX')`s'defn(`STREAMIDX')
')')dnl
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
          image: smtc_sensor_simulation:latest
          imagePullPolicy: IfNotPresent
          ports:
forloop(`CAMERAIDX',1,defn(`NCAMERAS2'),`dnl
            - containerPort: eval(defn(`CAMERA_RTSP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP'))
              protocol: TCP
forloop(`STREAMIDX',1,defn(`CAMERA_PORT_STEP'),`dnl
            - containerPort: eval(defn(`CAMERA_RTP_PORT')+defn(`CAMERAIDX')*defn(`CAMERA_PORT_STEP')-defn(`CAMERA_PORT_STEP')+defn(`STREAMIDX')-1)
              protocol: UDP
')')dnl
          env:
            - name: FILES
              value: "crowd.mp4$$"
            - name: `NCAMERAS'
              value: "defn(`NCAMERAS2')"
            - name: RTSP_PORT
              value: "defn(`CAMERA_RTSP_PORT')"
            - name: RTP_PORT
              value: "defn(`CAMERA_RTP_PORT')"
            - name: PORT_STEP
              value: "defn(`CAMERA_PORT_STEP')"
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
