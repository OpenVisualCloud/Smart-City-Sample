include(platform.m4)
define(`DB_NAME',ifelse(defn(`NOFFICES'),1,db,cloud-db))dnl

ifelse(index(`cloud',defn(`BUILD_SCOPE')),-1,,`

apiVersion: v1
kind: Service
metadata:
  name: defn(`DB_NAME')-service
  labels:
    app: defn(`DB_NAME')
spec:
  clusterIP: None
  ports:
  - port: 9200
    protocol: TCP
  selector:
    app: defn(`DB_NAME')

---

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: defn(`DB_NAME')
spec:
  serviceName: defn(`DB_NAME')
  replicas: defn(`HA_CLOUD')
  selector:
    matchLabels:
      app: defn(`DB_NAME')
  template:
    metadata:
      labels:
        app: defn(`DB_NAME')
        database: "yes"
    spec:
      enableServiceLinks: true
      containers:
        - name: defn(`DB_NAME')
          image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.13
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 9200
            - containerPort: 9300
          env:
ifelse(defn(`NOFFICES')defn(`HA_CLOUD'),11,`dnl
            - name: "discovery.type"
              value: "single-node"
',`dnl
            - name: "cluster.name"
              value: "cloud-cluster"
            - name: "node.name"
              value: "cloud-db"
            - name: "node.master"
              value: "true"
            - name: "node.data"
              value: "true"
            - name: "ES_JAVA_OPTS"
              value: "-Xms2048m -Xmx2048m"
            - name: "discovery.zen.minimum_master_nodes"
              value: "eval(defn(`HA_CLOUD')ifelse(eval(defn(`HA_CLOUD')%2),0,-1))"
            - name: "discovery.zen.ping.unicast.hosts"
              value: "defn(`DB_NAME')-service"
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
          lifecycle:
            preStop:
              exec:
                command: ["/usr/bin/curl","-X","DELETE","http://localhost:9200/offices,sensors_*"]
          securityContext:
            runAsUser: 1000
            runAsGroup: 1000
      initContainers:
        - name: init-volume-sysctl
          image: busybox:latest
          imagePullPolicy: IfNotPresent
          command: ["sh","-c","sysctl -w vm.max_map_count=262144 && ulimit -n 65535 && ulimit -u 4096"]
          securityContext:
            privileged: true
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
PLATFORM_NODE_SELECTOR(`Xeon')dnl
          podAntiAffinity:
            preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                  - key: database
                    operator: In
                    values:
                    - "yes"
                topologyKey: "kubernetes.io/hostname"

')
