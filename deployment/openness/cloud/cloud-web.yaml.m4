
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
          image: smtc_web_cloud:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8443
          env:
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,cloud-db,db)-service:9200"
            - name: `SCENARIO'
              value: "defn(`SCENARIO')"
            - name: HEALTH_CHECK
              value: "ifelse(eval(defn(`NOFFICES')>1),1,enabled,disabled)"
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
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        cloud-zone: "yes"
')dnl
