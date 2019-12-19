include(office.m4)

ifelse(defn(`SCENARIO_NAME'),`traffic',`dnl
apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-analytics
  labels:
     app: defn(`OFFICE_NAME')-analytics
spec:
  replicas: defn(`NANALYTICS')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-analytics
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-analytics
    spec:
      enableServiceLinks: false
ifelse(defn(`DISCOVER_IP_CAMERA'),`true',`dnl
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
')dnl
      containers:
        - name: defn(`OFFICE_NAME')-analytics
          image: `smtc_analytics_object_detection_xeon_'defn(`FRAMEWORK'):latest
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
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl
')dnl

ifelse(defn(`SCENARIO_NAME'),`stadium',`dnl
apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-analytics-people
  labels:
     app: defn(`OFFICE_NAME')-analytics-people
spec:
  replicas: defn(`NANALYTICS')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-analytics-people
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-analytics-people
    spec:
      enableServiceLinks: false
ifelse(defn(`DISCOVER_IP_CAMERA'),`true',`dnl
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
')dnl
      containers:
        - name: defn(`OFFICE_NAME')-analytics-people
          image: `smtc_analytics_people_counting_xeon_'defn(`FRAMEWORK'):latest
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
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl

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
          image: `smtc_analytics_crowd_counting_xeon_'defn(`FRAMEWORK'):latest
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
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-analytics-queue
  labels:
     app: defn(`OFFICE_NAME')-analytics-queue
spec:
  replicas: defn(`NANALYTICS3')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-analytics-queue
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-analytics-queue
    spec:
      enableServiceLinks: false
ifelse(defn(`DISCOVER_IP_CAMERA'),`true',`dnl
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
')dnl
      containers:
        - name: defn(`OFFICE_NAME')-analytics-queue
          image: `smtc_analytics_object_detection_xeon_'defn(`FRAMEWORK'):latest
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
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
ifelse(eval(defn(`NOFFICES')>1),1,`dnl
      nodeSelector:
        defn(`OFFICE_ZONE'): "yes"
')dnl
')dnl
