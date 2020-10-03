include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-gateway-service
  labels:
    app: defn(`OFFICE_NAME')-gateway
spec:
  ports:
  - port: 8080
    protocol: TCP
  selector:
    app: defn(`OFFICE_NAME')-gateway

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-gateway
  labels:
     app: defn(`OFFICE_NAME')-gateway
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-gateway
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-gateway
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-gateway
          image: defn(`REGISTRY_PREFIX')smtc_api_gateway:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080"
            - name: WEBRTCHOST
              value: "http://defn(`OFFICE_NAME')-webrtc-service:8888"
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
')')')
