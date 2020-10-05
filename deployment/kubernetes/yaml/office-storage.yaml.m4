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
  name: defn(`OFFICE_NAME')-storage-service
  labels:
    app: defn(`OFFICE_NAME')-storage
spec:
  ports:
  - port: 8080
    protocol: TCP
  selector:
    app: defn(`OFFICE_NAME')-storage

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-storage
  labels:
     app: defn(`OFFICE_NAME')-storage
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-storage
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-storage
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-storage
          image: defn(`REGISTRY_PREFIX')smtc_storage_manager:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: INDEXES
              value: "recordings,analytics"
            - name: RETENTION_TIME
              value: "3600"
            - name: SERVICE_INTERVAL
              value: "1800"
            - name: WARN_DISK
              value: "70"
            - name: FATAL_DISK
              value: "75"
            - name: HALT_REC
              value: "80"
            - name: THUMBNAIL_CACHE
              value: "50"
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
