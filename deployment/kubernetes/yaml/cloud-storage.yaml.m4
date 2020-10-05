include(platform.m4)

ifelse(index(`cloud',defn(`BUILD_SCOPE')),-1,,`

apiVersion: v1
kind: Service
metadata:
  name: cloud-storage-service
  labels:
    app: cloud-storage
spec:
  ports:
  - port: 8080
    protocol: TCP
  selector:
    app: cloud-storage

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloud-storage
  labels:
     app: cloud-storage
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cloud-storage
  template:
    metadata:
      labels:
        app: cloud-storage
    spec:
      enableServiceLinks: false
      containers:
        - name: cloud-storage
          image: defn(`REGISTRY_PREFIX')smtc_storage_manager:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,cloud-db)-service:9200"
            - name: INDEXES
              value: "recordings"
            - name: RETENTION_TIME
              value: "7200"
            - name: SERVICE_INTERVAL
              value: "3600"
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

')
