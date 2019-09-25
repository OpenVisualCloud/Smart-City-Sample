
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: cloud-web-service-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /
        backend:
          serviceName: cloud-web-service
          servicePort: 8080

---

apiVersion: v1
kind: Service
metadata:
  name: cloud-web-service
  labels:
    app: cloud-web
spec:
  ports:
    - port: 8080
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
      containers:
        - name: cloud-web
          image: smtc_web_cloud:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,cloud-db,db)-service:9200"
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
#      nodeSelector:
#        "kubernetes.io/hostname": "defn(`HOSTNAME')"
