include(office.m4)

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
            - name:  "transport.host"
              value: "0.0.0.0"
            - name:  "transport.port"
              value: "9300"
            - name:  "transport.publish_host"
              value: "defn(`CLOUD_HOST')"
            - name:  "transport.publish_port"
              value: "eval(30300 + defn(`OFFICEIDX'))"
            - name: "discovery.zen.minimum_master_nodes"
              value: "1"
            - name: "discovery.zen.ping.unicast.hosts"
              value: "defn(`CLOUD_HOST'):30300"
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
            - mountPath: /usr/share/elasticsearch/data
              name: defn(`OFFICE_NAME')-esdata
      initContainers:
        - name: init-volume-sysctl
          image: busybox:latest
          command: ["sh","-c","sysctl -w vm.max_map_count=262144"]
          securityContext:
            privileged: true
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
          - name: defn(`OFFICE_NAME')-esdata
            emptyDir: {}
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl

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
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: PROXYHOST
              value: "http://defn(`CLOUD_HOST'):eval(8080 + defn(`OFFICEIDX'))"
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
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl
