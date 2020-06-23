include(platform.m4)
define(`DB_NAME',ifelse(eval(defn(`NOFFICES')>1),1,cloud-db,db))dnl

ifelse(index(`cloud',defn(`BUILD_SCOPE')),-1,,`

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
      enableServiceLinks: false
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
              value: "true"
            - name: "node.attr.zone"
              value: "cloud"
            - name: "ES_JAVA_OPTS"
              value: "-Xms2048m -Xmx2048m"
',`dnl
            - name: "discovery.type"
              value: "single-node"
')dnl
            - name: "action.auto_create_index"
              value: "0"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
      initContainers:
        - name: init-volume-sysctl
          image: busybox:latest
          command: ["sh","-c","sysctl -w vm.max_map_count=262144 && ulimit -n 65535 && ulimit -u 4096"]
          securityContext:
            privileged: true
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
PLATFORM_NODE_SELECTOR(`Xeon')dnl

')
