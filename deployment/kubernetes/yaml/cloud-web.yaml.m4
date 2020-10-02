include(platform.m4)

ifelse(index(`cloud',defn(`BUILD_SCOPE')),-1,,`

apiVersion: v1
kind: Service
metadata:
  name: cloud-web-service
  labels:
    app: cloud-web
spec:
  ports:
    - port: 443
      targetPort: 8443
      name: https
  externalIPs:
    - defn(`HOSTIP')
  selector:
    app: cloud-web

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloud-web
  labels:
     app: cloud-web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cloud-web
  template:
    metadata:
      labels:
        app: cloud-web
    spec:
      enableServiceLinks: false
      containers:
        - name: cloud-web
          image: defn(`REGISTRY_PREFIX')smtc_web_cloud:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8443
          env:
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,cloud-db)-service:9200"
            - name: `SCENARIO'
              value: "defn(`SCENARIO')"
            - name: GWHOST
              value: "http://cloud-gateway-service:8080"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /var/run/secrets
              name: self-signed-certificate
              readOnly: true
      volumes:
        - name: timezone
          hostPath:
            path: /etc/localtime
            type: File
        - name: self-signed-certificate
          secret:
            secretName: self-signed-certificate
PLATFORM_NODE_SELECTOR(`Xeon')dnl

')
