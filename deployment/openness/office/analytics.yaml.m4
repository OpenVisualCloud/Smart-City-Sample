include(office.m4)
include(platform.m4)

ifelse(defn(`SCENARIO_NAME'),`traffic',`dnl
apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-analytics-traffic
  labels:
     app: defn(`OFFICE_NAME')-analytics-traffic
spec:
  replicas: defn(`NANALYTICS')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-analytics-traffic
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-analytics-traffic
    spec:
      enableServiceLinks: false
ifelse(defn(`DISCOVER_IP_CAMERA'),`true',`dnl
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
')dnl
      containers:
        - name: defn(`OFFICE_NAME')-analytics-traffic
          image: `smtc_analytics_object_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/api/upload"
            - name: EVERY_NTH_FRAME
              value: "6"
            - name: `SCENARIO'
              value: "defn(`SCENARIO')"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
defn(`PLATFORM_VOLUME_MOUNTS')dnl
      volumes:
          - name: timezone
            hostPath:
              path: /etc/localtime
              type: File
defn(`PLATFORM_VOLUMES')dnl
PLATFORM_NODE_SELECTOR(`VCAC-A')dnl
')dnl

ifelse(defn(`SCENARIO_NAME'),`stadium',`dnl
apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-analytics-entrance
  labels:
     app: defn(`OFFICE_NAME')-analytics-entrance
spec:
  replicas: defn(`NANALYTICS')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-analytics-entrance
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-analytics-entrance
    spec:
      enableServiceLinks: false
ifelse(defn(`DISCOVER_IP_CAMERA'),`true',`dnl
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
')dnl
      containers:
        - name: defn(`OFFICE_NAME')-analytics-entrance
          image: `smtc_analytics_entrance_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/api/upload"
            - name: EVERY_NTH_FRAME
              value: "6"
            - name: `SCENARIO'
              value: "defn(`SCENARIO')"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
defn(`PLATFORM_VOLUME_MOUNTS')dnl
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
defn(`PLATFORM_VOLUMES')dnl
PLATFORM_NODE_SELECTOR(`VCAC-A')dnl

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-analytics-crowd
  labels:
     app: defn(`OFFICE_NAME')-analytics-crowd
spec:
  replicas: defn(`NANALYTICS2')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-analytics-crowd
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-analytics-crowd
    spec:
      enableServiceLinks: false
ifelse(defn(`DISCOVER_IP_CAMERA'),`true',`dnl
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
')dnl
      containers:
        - name: defn(`OFFICE_NAME')-analytics-crowd
          image: `smtc_analytics_crowd_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/api/upload"
            - name: EVERY_NTH_FRAME
              value: "30"
            - name: `SCENARIO'
              value: "defn(`SCENARIO')"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
defn(`PLATFORM_VOLUME_MOUNTS')dnl
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
defn(`PLATFORM_VOLUMES')dnl
PLATFORM_NODE_SELECTOR(`VCAC-A')dnl

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-analytics-svcq
  labels:
     app: defn(`OFFICE_NAME')-analytics-svcq
spec:
  replicas: defn(`NANALYTICS3')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-analytics-svcq
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-analytics-svcq
    spec:
      enableServiceLinks: false
ifelse(defn(`DISCOVER_IP_CAMERA'),`true',`dnl
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
')dnl
      containers:
        - name: defn(`OFFICE_NAME')-analytics-svcq
          image: `smtc_analytics_object_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/api/upload"
            - name: EVERY_NTH_FRAME
              value: "6"
            - name: `SCENARIO'
              value: "defn(`SCENARIO')"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
defn(`PLATFORM_VOLUME_MOUNTS')dnl
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
defn(`PLATFORM_VOLUMES')dnl
PLATFORM_NODE_SELECTOR(`VCAC-A')dnl
')
