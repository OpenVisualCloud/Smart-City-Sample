include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

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
          image: defn(`REGISTRY_PREFIX')`smtc_analytics_object_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/api/upload"
            - name: MQTT_TOPIC
              value: "ifelse(defn(`OT_TYPE'),`false',analytics,relayanalytics)"
            - name: EVERY_NTH_FRAME
              value: "6"
            - name: `SCENARIO'
              value: "defn(`SCENARIO_NAME')"
            - name: `NETWORK_PREFERENCE'
              value: "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            - name: GST_DEBUG
              value: "3"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /tmp/rec
              name: recording
defn(`PLATFORM_VOLUME_MOUNTS')dnl
      initContainers:
            - image: busybox:latest
              imagePullPolicy: IfNotPresent
              name: init
              command: ["/bin/chown","defn(`USERID'):defn(`GROUPID')","/tmp/rec"]
              volumeMounts:
                - mountPath: /tmp/rec
                  name: recording
      volumes:
          - name: timezone
            hostPath:
              path: /etc/localtime
              type: File
          - name: recording
            emptyDir:
              medium: Memory
              sizeLimit: 150Mi
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
  replicas: defn(`NANALYTICS3')
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
          image: defn(`REGISTRY_PREFIX')`smtc_analytics_entrance_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/api/upload"
            - name: MQTT_TOPIC
              value: "ifelse(defn(`OT_TYPE'),`false',analytics,relayanalytics)"
            - name: EVERY_NTH_FRAME
              value: "6"
            - name: `SCENARIO'
              value: "defn(`SCENARIO_NAME')"
            - name: `NETWORK_PREFERENCE'
              value: "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /tmp/rec
              name: recording
defn(`PLATFORM_VOLUME_MOUNTS')dnl
      initContainers:
            - image: busybox:latest
              imagePullPolicy: IfNotPresent
              name: init
              command: ["/bin/chown","defn(`USERID'):defn(`GROUPID')","/tmp/rec"]
              volumeMounts:
                - mountPath: /tmp/rec
                  name: recording
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
          - name: recording
            emptyDir:
              medium: Memory
              sizeLimit: 150Mi
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
          image: defn(`REGISTRY_PREFIX')`smtc_analytics_crowd_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/api/upload"
            - name: MQTT_TOPIC
              value: "analytics"
            - name: EVERY_NTH_FRAME
              value: "6"
            - name: `SCENARIO'
              value: "defn(`SCENARIO_NAME')"
            - name: `NETWORK_PREFERENCE'
              value: "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /tmp/rec
              name: recording
defn(`PLATFORM_VOLUME_MOUNTS')dnl
      initContainers:
            - image: busybox:latest
              imagePullPolicy: IfNotPresent
              name: init
              command: ["/bin/chown","defn(`USERID'):defn(`GROUPID')","/tmp/rec"]
              volumeMounts:
                - mountPath: /tmp/rec
                  name: recording
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
          - name: recording
            emptyDir:
              medium: Memory
              sizeLimit: 150Mi
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
  replicas: defn(`NANALYTICS')
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
          image: defn(`REGISTRY_PREFIX')`smtc_analytics_object_'defn(`PLATFORM_SUFFIX')`_'defn(`FRAMEWORK'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(defn(`NOFFICES'),1,db,defn(`OFFICE_NAME')-db)-service:9200"
            - name: MQTTHOST
              value: "defn(`OFFICE_NAME')-mqtt-service"
            - name: STHOST
              value: "http://defn(`OFFICE_NAME')-storage-service:8080/api/upload"
            - name: MQTT_TOPIC
              value: "ifelse(defn(`OT_TYPE'),`false',analytics,relayanalytics)"
            - name: EVERY_NTH_FRAME
              value: "6"
            - name: `SCENARIO'
              value: "defn(`SCENARIO_NAME')"
            - name: `NETWORK_PREFERENCE'
              value: "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /tmp/rec
              name: recording
defn(`PLATFORM_VOLUME_MOUNTS')dnl
      initContainers:
            - image: busybox:latest
              imagePullPolicy: IfNotPresent
              name: init
              command: ["/bin/chown","defn(`USERID'):defn(`GROUPID')","/tmp/rec"]
              volumeMounts:
                - mountPath: /tmp/rec
                  name: recording
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
          - name: recording
            emptyDir:
              medium: Memory
              sizeLimit: 150Mi
defn(`PLATFORM_VOLUMES')dnl
PLATFORM_NODE_SELECTOR(`VCAC-A')dnl
')

---
')')')
