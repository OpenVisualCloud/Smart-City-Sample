
apiVersion: v1
kind: Service
metadata:
  name: cloud-web-service
  labels:
    app: cloud-web
spec:
  type: NodePort
  ports:
  - port: 8080
    nodePort: 30443
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
          image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: "DBHOST"
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
      volumes:
        - name: timezone
          hostPath:
            path: /etc/localtime
              type: File
        - name: self-signed-certificate
          secret:
            secretName: self-signed-certificate
      nodeSelector:
        "kubernetes.io/hostname": "defn(`HOSTNAME')"
