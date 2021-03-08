include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

ifelse(defn(`NOFFICES'),1,,`dnl

apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-db-service
  labels:
    app: defn(`OFFICE_NAME')-db
spec:
  clusterIP: None
  ports:
  - port: 9200
    protocol: TCP
  selector:
    app: defn(`OFFICE_NAME')-db

---

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: defn(`OFFICE_NAME')-db
  labels:
     app: defn(`OFFICE_NAME')-db
spec:
  serviceName: defn(`OFFICE_NAME')-db
  replicas: defn(`HA_OFFICE')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-db
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-db
        database: "yes"
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-db
          image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.13
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 9200
            - containerPort: 9300
          env:
            - name: "cluster.name"
              value: "office-cluster"
            - name: "node.name"
              value: "defn(`OFFICE_NAME')"
            - name: "node.master"
              value: "true"
            - name: "node.data"
              value: "true"
            - name: "discovery.zen.minimum_master_nodes"
              value: "eval(defn(`HA_OFFICE')ifelse(eval(defn(`HA_OFFICE')%2),0,-1))"
            - name: "discovery.zen.ping.unicast.hosts"
              value: "defn(`OFFICE_NAME')-db-service"
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
          lifecycle:
            preStop:
              exec:
                command: ["/usr/bin/curl","-X","DELETE","http://localhost:9200/sensors_*"]
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

---

')dnl

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-db-init
  labels:
      app: defn(`OFFICE_NAME')-db-init
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-db-init
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-db-init
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-db-init
          image: defn(`REGISTRY_PREFIX')smtc_db_init:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: "OFFICE"
              value: "defn(`OFFICE_LOCATION')"
            - name: "DBHOST"
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: "DBCHOST"
              value: "http://cloud-gateway-service:8080/cloud/api/db"
            - name: GWHOST
              value: "http://defn(`OFFICE_NAME')-gateway-service:8080"
            - name: `SCENARIO'
              value: "defn(`SCENARIO_NAME')"
            - name: REPLICAS
              value: "ifelse(defn(`HA_CLOUD'),1,0,1),ifelse(defn(`HA_OFFICE'),1,0,1)"
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
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
          - name: sensor-info
            configMap:
                name: sensor-info
PLATFORM_NODE_SELECTOR(`Xeon')dnl
          podAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)
              topologyKey: "kubernetes.io/hostname"

---
')')')
