
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
          image: smtc_storage_manager:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,cloud-db,db)-service:9200"
            - name: PROXYHOST
              value: "http://cloud-storage-service.default.svc.cluster.local:8080"
            - name: INDEXES
              value: "recordings_c"
            - name: RETENTION_TIME
              value: "7200"
            - name: SERVICE_INTERVAL
              value: "7200"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /var/www
              name: cloud-stdata
      initContainers:
        - name: cloud-storage-init
          image: centos:7.6.1810
          command: ["sh","-c","mkdir -p /var/www/log /var/www/tmp /var/www/cache /var/www/upload /var/www/mp4 && chown -R defn(`USERID').defn(`GROUPID') /var/www"]
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /var/www
              name: cloud-stdata
      volumes:
        - name: timezone
          hostPath:
            path: /etc/localtime
            type: File
        - name: cloud-stdata
          emptyDir: {}
