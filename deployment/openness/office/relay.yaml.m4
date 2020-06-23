include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-relay
  labels:
     app: defn(`OFFICE_NAME')-relay
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-relay
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-relay
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-relay
          image: smtc_relay:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: RELAY_NUMBER
              value: "2"
            - name: RELAY1_SRC_HOST
              value: "defn(`CLOUD_HOST')"
            - name: RELAY1_SRC_PORT
              value: "eval(30300 + defn(`OFFICEIDX'))"
            - name: RELAY1_DST_HOST
              value: "ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service"
            - name: RELAY1_DST_PORT
              value: "9300"
            - name: RELAY2_SRC_HOST
              value: "defn(`CLOUD_HOST')"
            - name: RELAY2_SRC_PORT
              value: "eval(8080 + defn(`OFFICEIDX'))"
            - name: RELAY2_DST_HOST
              value: "defn(`OFFICE_NAME')-storage-service.default.svc.cluster.local"
            - name: RELAY2_DST_PORT
              value: "8080"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /etc/relay-key-pair
              name: relay-key-pair-secret
              readOnly: true
      volumes:
          - name: relay-key-pair-secret
            secret:
                secretName: relay-key-pair-secret
                defaultMode: 256
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
PLATFORM_NODE_SELECTOR(`Xeon')dnl

---
')')')
