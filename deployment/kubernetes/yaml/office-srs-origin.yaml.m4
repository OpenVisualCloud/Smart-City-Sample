include(platform.m4)
include(../../../script/loop.m4)
include(../../../maintenance/db-init/sensor-info.m4)

looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(OFFICEIDX,1,defn(`NOFFICES'),`
include(office.m4)
ifelse(len(defn(`OFFICE_LOCATION')),0,,`

ifelse(defn(`DISCOVER_RTMP'),`true',`dnl

apiVersion: v1
kind: ConfigMap
metadata:
  name: defn(`OFFICE_NAME')-srs-origin-config
data:
  srs.conf: |-
    listen              1935;
    max_connections     1000;
    daemon              off;
    http_api {
        enabled         on;
        listen          1985;
    }
    http_server {
        enabled         on;
        listen          8080;
        dir             ./objs/nginx/html;
    }
    stream_caster {
        enabled             on;
        caster              gb28181;
        output              rtmp://127.0.0.1:1935/live/[stream];
        listen              9000;
        rtp_port_min        58200;
        rtp_port_max        58300;
        wait_keyframe       on;
        rtp_idle_timeout    30;
        audio_enable        off;
        jitterbuffer_enable  on;
        host   defn(`HOSTIP');
        auto_create_channel   off;

        sip {
            enabled on;
            listen              5060;
            serial              34020000002000000001;
            realm               3402000000;
            ack_timeout         30;
            keepalive_timeout   120;
            auto_play           on;
            invite_port_fixed     on;
            query_catalog_interval  60;
        }
    }
    vhost __defaultVhost__ {
        cluster {
            origin_cluster  on;
            coworkers       loop(`SRSIDX',0,eval(defn(`HA_SRS_OFFICE')-1),`defn(`OFFICE_NAME')-srs-origin-defn(`SRSIDX').socs ')  ;
        }
        http_remux {
            enabled     on;
        }
        hls {
            enabled     on;
        }
    }

---

apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-srs-origin-service
  labels:
    app: defn(`OFFICE_NAME')-srs
spec:
  ports:
    - name: srs-service-1935-1935
      port: 1935
      protocol: TCP
      targetPort: 1935
    - name: srs-service-9000-9000
      port: 9000
      protocol: UDP 
      targetPort: 9000
    - name: srs-service-5060-5060
      port: 5060
      protocol: UDP
      targetPort: 5060
  externalIPs:
    - defn(`HOSTIP')
  selector:
    app: defn(`OFFICE_NAME')-srs-origin

---

loop(`SRSIDX',0,eval(defn(`HA_SRS_OFFICE')-1),`dnl
apiVersion: v1
kind: Service
metadata:
  name: defn(`OFFICE_NAME')-srs-origin-defn(`SRSIDX')-api-service
  labels:
    app: defn(`OFFICE_NAME')-srs
spec:
  ports:
    - name: srs-service-1985-1985
      port: 1985
      protocol: TCP
      targetPort: 1985
  selector:
    statefulset.kubernetes.io/pod-name: defn(`OFFICE_NAME')-srs-origin-defn(`SRSIDX')
---

')dnl

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: defn(`OFFICE_NAME')-srs-origin
  labels:
     app: defn(`OFFICE_NAME')-srs-origin
spec:
  serviceName: "socs"
  replicas: defn(`HA_SRS_OFFICE')
  selector:
    matchLabels:
      app: defn(`OFFICE_NAME')-srs-origin
  template:
    metadata:
      labels:
        app: defn(`OFFICE_NAME')-srs-origin
    spec:
      enableServiceLinks: false
      containers:
        - name: defn(`OFFICE_NAME')-srs-origin
          image: defn(`REGISTRY_PREFIX')smtc_sensor_srs:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 1935
            - containerPort: 1985
            - containerPort: 8080
            - containerPort: 9000 
            - containerPort: 5060
          env:
            - name: EIP
              value: "defn(`HOSTIP')"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /var/www/video
              name: video-archive
            - mountPath: /usr/local/srs/conf
              name: config-volume
          resources:
            limits:
              cpu: "4"
      volumes:
          - name: timezone
            hostPath:
                path: /etc/localtime
                type: File
          - name: config-volume
            configMap:
              name: defn(`OFFICE_NAME')-srs-origin-config
          - name: video-archive
            emptyDir:
              medium: Memory
              sizeLimit: 150Mi
PLATFORM_NODE_SELECTOR(`Xeon')dnl

---



')')')')
