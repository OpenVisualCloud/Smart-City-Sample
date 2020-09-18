include(platform.m4)

ifelse(index(`cloud',defn(`BUILD_SCOPE')),-1,,`

apiVersion: v1
kind: Service
metadata:
  name: cloud-gateway-service
  labels:
    app: cloud-gateway
spec:
  ports:
  - port: 8080
    protocol: TCP
  selector:
    app: cloud-gateway

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloud-gateway
  labels:
     app: cloud-gateway
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cloud-gateway
  template:
    metadata:
      labels:
        app: cloud-gateway
    spec:
      enableServiceLinks: false
      containers:
        - name: cloud-gateway
          image: defn(`REGISTRY_PREFIX')smtc_api_gateway:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,cloud-db)-service:9200"
            - name: STHOST
              value: "http://cloud-storage-service:8080"
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
