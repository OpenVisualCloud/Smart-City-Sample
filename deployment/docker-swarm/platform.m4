define(`PLATFORM_SUFFIX',translit(defn(`PLATFORM'),`A-Z',`a-z'))dnl
define(`PLATFORM_IMAGE',`ifelse(defn(`PLATFORM'),`VCAC-A',defn(`REGISTRY_PREFIX')vcac-container-launcher:latest,define(`_PLATFORM_IMAGE',$1)$1)')dnl
define(`PLATFORM_VOLUME_EXTRA',ifelse(defn(`PLATFORM'),`VCAC-A',dnl
            - /var/run/docker.sock:/var/run/docker.sock
))dnl
define(`PLATFORM_ENV_EXTRA',`ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
            VCAC_IMAGE: defn(`_PLATFORM_IMAGE')
')')dnl
define(`PLATFORM_ENV',ifelse(defn(`PLATFORM'),`VCAC-A',`VCAC_'$1,$1))dnl
define(`PLATFORM_ZONE',`node.labels.vcac_zone ifelse(defn(`PLATFORM'),`VCAC-A',`==',`!=') yes')dnl
define(`PLATFORM_DEVICE',ifelse(defn(`PLATFORM'),`VCAC-A',`HDDL',`CPU'))dnl
