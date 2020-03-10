define(`PLATFORM_SUFFIX',translit(defn(`PLATFORM'),`A-Z',`a-z'))dnl
define(`PLATFORM_VOLUME_MOUNTS',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
            - mountPath: /var/tmp
              name: var-tmp
#          resources:
#            limits:
#              vpu.intel.com/hddl: 1
#              gpu.intel.com/i915: 1
          securityContext:
            privileged: true
))dnl
define(`PLATFORM_VOLUMES',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
          - name: var-tmp
            hostPath:
              path: /var/tmp
              type: Directory
))dnl
define(`PLATFORM_NODE_SELECTOR',dnl
      affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
                - matchExpressions:
                  - key: "vcac-zone"
                    operator: `ifelse(defn(`PLATFORM'),$1,`In',`NotIn')'
                    values:
                      - "yes"
)dnl
