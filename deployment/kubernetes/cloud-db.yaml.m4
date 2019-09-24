define(`DB_NAME',ifelse(eval(defn(`NOFFICES')>1),1,cloud-db,db))dnl

apiVersion: v1
kind: Service
metadata:
  name: defn(`DB_NAME')-service
  labels:
    app: defn(`DB_NAME')
spec:
  ports:
  - port: 9200
    protocol: TCP
    name: dsl
  - port: 9300
    protocol: TCP
    name: transport
  selector:
    app: defn(`DB_NAME')

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`DB_NAME')
  labels:
     app: defn(`DB_NAME')
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`DB_NAME')
  template:
    metadata:
      labels:
        app: defn(`DB_NAME')
    spec:
      containers:
        - name: defn(`DB_NAME')
          image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 9200
            - containerPort: 9300
          env:
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
            - name: "cluster.name"
              value: "db-cluster"
            - name: "node.name"
              value: "cloud-db"
            - name: "node.master"
              value: "true"
            - name: "node.data"
              value: "false"
',`dnl
            - name: "discovery.type"
              value: "single-node"
')dnl
            - name: "action.auto_create_index"
              value: "0"
            - name: "ES_JAVA_OPTS"
              value: "-Xms4096m -Xmx4096m"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /usr/share/elasticsearch/data
              name: defn(`DB_NAME')-esdata
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
          - name: defn(`DB_NAME')-esdata
            emptyDir: {}
