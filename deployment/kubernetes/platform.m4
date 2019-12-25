define(`PLATFORM_SUFFIX',translit(defn(`PLATFORM'),`A-Z',`a-z'))dnl
define(`PLATFORM_VOLUME_MOUNTS',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
            - mountPath: /var/tmp/hddl_service.sock
              name: hddl-sock-mount
            - mountPath: /var/tmp/hddl_service_ready.mutex
              name: hddl-ready-mount
            - mountPath: /var/tmp/hddl_service_alive.mutex
              name: hddl-alive-mount
))dnl
define(`PLATFORM_VOLUMES',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
          - name: hddl-sock-mount
            hostPath:
              path: /var/tmp/hddl_service.sock
          - name: hddl-ready-mount
            hostPath:
              path: /var/tmp/hddl_service_ready.mutex
          - name: hddl-alive-mount
            hostPath:
              path: /var/tmp/hddl_service_alive.mutex
))dnl
define(`PLATFORM_NODE_SELECTOR',dnl
`ifelse("$@ifelse(defn(`PLATFORM'),`VCAC-A',emit)","",,dnl
      nodeSelector:
)'dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
          vcac-zone: "yes"
)dnl
$@
)dnl
