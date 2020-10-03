include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)
define(`WEBRTC_UDP_PORT',10000)
define(`WEBRTC_STREAMING_LIMIT',10)

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
      port: eval(defn(`WEBRTC_UDP_PORT')+defn(`PORTIDX'))
      targetPort: eval(defn(`WEBRTC_UDP_PORT')+defn(`PORTIDX'))
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
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
          securityContext:
            runAsUser: 103
        - name: mongodb
          image: defn(`REGISTRY_PREFIX')smtc_sensor_webrtc:latest
          imagePullPolicy: IfNotPresent
          command: [ "/usr/bin/mongod","--config","/etc/mongodb.conf" ]
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
          securityContext:
            runAsUser: 102
        - name: webrtc
          image: defn(`REGISTRY_PREFIX')smtc_sensor_webrtc:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8888
loop(PORTIDX,1,defn(`WEBRTC_STREAMING_LIMIT'),`dnl
            - containerPort: eval(defn(`WEBRTC_UDP_PORT')+defn(`PORTIDX'))
              protocol: UDP
')dnl
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: `WEBRTC_STREAMING_LIMIT'
              value: "defn(`WEBRTC_STREAMING_LIMIT')"
            - name: `WEBRTC_UDP_PORT'
              value: "defn(`WEBRTC_UDP_PORT')"
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
            runAsUser: 1000
      volumes:
          - name: timezone
            hostPath:
              path: /etc/localtime
              type: File
PLATFORM_NODE_SELECTOR(`Xeon')dnl

---
')
define(`WEBRTC_UDP_PORT',eval(defn(`WEBRTC_UDP_PORT')+defn(`WEBRTC_STREAMING_LIMIT')))
')')
