include(office.m4)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: defn(`OFFICE_NAME')-where-indexing
  labels:
     app: defn(`OFFICE_NAME')-where-indexing
spec:
  replicas: 1
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-where-indexing
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-where-indexing
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-where-indexing
          image: smtc_where_indexing:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: INDEXES
              value: "recordings,analytics"
            - name: OFFICE
              value: "defn(`OFFICE_LOCATION')"
            - name: DBHOST
              value: "http://ifelse(eval(defn(`NOFFICES')>1),1,defn(`OFFICE_NAME')-db,db)-service:9200"
            - name: SERVICE_INTERVAL
              value: "30"
            - name: UPDATE_INTERVAL
              value: "5"
            - name: SEARCH_BATCH
              value: "3000"
            - name: UPDATE_BATCH
              value: "500"
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
