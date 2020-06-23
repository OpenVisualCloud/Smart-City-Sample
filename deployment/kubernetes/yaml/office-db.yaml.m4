include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

ifelse(eval(defn(`NOFFICES')>1),1,`dnl

apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-db-service
  labels:
    app: defn(`OFFICE_NAME')-db
spec:
  ports:
  - port: 9200
    protocol: TCP
    name: dsl
  - port: 9300
    protocol: TCP
    name: transport
  selector:
    app: defn(`OFFICE_NAME')-db

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-db
  labels:
     app: defn(`OFFICE_NAME')-db
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-db
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-db
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-db
          image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 9200
            - containerPort: 9300
          env:
            - name: "cluster.name"
              value: "db-cluster"
            - name: "node.name"
              value: "defn(`OFFICE_NAME')"
            - name: "node.master"
              value: "false"
            - name: "node.data"
              value: "true"
            - name: "node.attr.zone"
              value: "defn(`OFFICE_NAME')"
            - name: "discovery.zen.minimum_master_nodes"
              value: "1"
            - name: "discovery.zen.ping.unicast.hosts"
              value: "cloud-db-service"
            - name: "action.auto_create_index"
              value: "0"
            - name: "ES_JAVA_OPTS"
              value: "-Xms2048m -Xmx2048m"
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

---

')dnl

apiVersion: batch/v1
kind: Job
metadata:
  name: defn(`OFFICE_NAME')-db-init
spec:
  template:
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-db-init
          image: smtc_db_init:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: "OFFICE"
              value: "defn(`OFFICE_LOCATION')"
            - name: "DBHOST"
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,cloud-)db-service:9200"
            - name: PROXYHOST
              value: "http://defn(`OFFICE_NAME')-storage-service.default.svc.cluster.local:8080"
            - name: `SCENARIO'
              value: "defn(`SCENARIO_NAME')"
            - name: "ZONE"
              value: "defn(`OFFICE_NAME')"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /var/run/secrets
              name: sensor-info
              readOnly: true
      restartPolicy: Never
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
          - name: sensor-info
            configMap:
                name: sensor-info
PLATFORM_NODE_SELECTOR(`Xeon')dnl

---
')')')
