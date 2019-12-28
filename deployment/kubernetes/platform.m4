define(`PLATFORM_SUFFIX',translit(defn(`PLATFORM'),`A-Z',`a-z'))dnl
define(`PLATFORM_VOLUME_MOUNTS',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
            - mountPath: /var/tmp
              name: var-tmp
            - mountPath: /tmp
              name: tmp
            - mountPath: /dev/ion
              name: dev-ion
          securityContext:
            privileged: true
))dnl
define(`PLATFORM_VOLUMES',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
          - name: var-tmp
            hostPath:
              path: /var/tmp
              type: Directory
          - name: tmp
            hostPath:
              path: /tmp
              type: Directory
          - name: dev-ion
            hostPath:
              path: /dev/ion
              type: CharDevice
))dnl
define(`PLATFORM_NODE_SELECTOR',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
      nodeSelector:
          vcac-zone: "yes"
)dnl
)dnl
