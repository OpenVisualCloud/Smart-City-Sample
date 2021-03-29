include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

define(`UDPBASE',0)
looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-webrtc-service
  labels:
    app: defn(`OFFICE_NAME')-webrtc
spec:
  ports:
    - port: 8888
      targetPort: 8888
  selector:
    app: defn(`OFFICE_NAME')-webrtc

---

apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-webrtc-io-service
  labels:
    app: defn(`OFFICE_NAME')-webrtc-io
spec:
  ports:
loop(PORTIDX,1,defn(`WEBRTC_STREAMING_LIMIT'),`dnl
    - name: `port'defn(`PORTIDX')
      protocol: UDP
      port: eval(defn(`WEBRTC_UDP_PORT')+defn(`UDPBASE')+defn(`PORTIDX'))
      targetPort: eval(defn(`WEBRTC_UDP_PORT')+defn(`UDPBASE')+defn(`PORTIDX'))
')dnl
  externalIPs:
    - defn(`HOSTIP')
  selector:
    app: defn(`OFFICE_NAME')-webrtc

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-webrtc
  labels:
     app: defn(`OFFICE_NAME')-webrtc
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-webrtc
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-webrtc
    spec:
      enableServiceLinks: false
      containers:
        - name: rabbitmq
          image: defn(`REGISTRY_PREFIX')smtc_sensor_webrtc:latest
          imagePullPolicy: IfNotPresent
          command: [ "/usr/sbin/rabbitmq-server" ]
          env:
            - name: RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS
              value: "+sbwt none"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
          securityContext:
            runAsUser: 106
        - name: mongodb
          image: defn(`REGISTRY_PREFIX')smtc_sensor_webrtc:latest
          imagePullPolicy: IfNotPresent
          command: [ "/usr/bin/mongod","--config","/etc/mongodb.conf" ]
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
          securityContext:
            runAsUser: 105
        - name: webrtc
          image: defn(`REGISTRY_PREFIX')smtc_sensor_webrtc:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8888
loop(PORTIDX,1,defn(`WEBRTC_STREAMING_LIMIT'),`dnl
            - containerPort: eval(defn(`WEBRTC_UDP_PORT')+defn(`UDPBASE')+defn(`PORTIDX'))
              protocol: UDP
')dnl
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: RTMP_HOST
              value: "rtmp://defn(`OFFICE_NAME')-rtmp-service:1935/sensors"
            - name: `WEBRTC_STREAMING_LIMIT'
              value: "defn(`WEBRTC_STREAMING_LIMIT')"
            - name: `WEBRTC_UDP_PORT'
              value: "eval(defn(`WEBRTC_UDP_PORT')+defn(`UDPBASE'))"
            - name: INACTIVE_TIME
              value: "10"
            - name: WEBRTC_HOSTIP
              value: "defn(`HOSTIP')"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
          resources:
            limits:
              cpu: "4"
            requests:
              cpu: "0.5"
          securityContext:
            runAsUser: defn(`USERID')
      volumes:
          - name: timezone
            hostPath:
              path: /etc/localtime
              type: File
PLATFORM_NODE_SELECTOR(`Xeon')dnl

---
')
define(`UDPBASE',eval(defn(`UDPBASE')+defn(`WEBRTC_STREAMING_LIMIT')))
')')
