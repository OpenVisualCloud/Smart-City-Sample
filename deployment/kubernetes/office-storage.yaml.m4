include(office.m4)

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
          image: smtc_storage_manager:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: INDEXES
              value: "recordings,analytics"
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
              name: defn(`OFFICE_NAME')-stdata
      initContainers:
        - name: storage-init
          image: busybox:latest
          command: ["sh","-c","mkdir -p /var/www/log /var/www/tmp /var/www/cache /var/www/upload /var/www/mp4 && chown -R defn(`USERID').defn(`GROUPID') /var/www"]
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /var/www
              name: defn(`OFFICE_NAME')-stdata
      volumes:
        - name: timezone
          hostPath:
            path: /etc/localtime
            type: File
        - name: defn(`OFFICE_NAME')-stdata
          emptyDir: {}
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`STORAGE_ZONE'): "yes" 
        defn(`OFFICE_ZONE'): "yes"
')dnl
