include(../common/forloop.m4)
include(../common/location.m4)

version: "3.7"

services:

include(cloud-db.m4)
include(cloud-web.m4)

forloop(`id',1,defn(`NOFFICES'),`
define(`OFFICE_NAME',`office'defn(`id'))
ifdef(`location_'defn(`OFFICE_NAME'),`
define(`OFFICE_LOCATION',defn(`location_'defn(`OFFICE_NAME')))
define(`CAMERA_NETWORK',192.168.defn(`id').0/24)
include(camera.m4)
include(office-db.m4)
include(camera-discovery.m4)
include(health-check.m4)
include(where-indexing.m4)
include(office-storage.m4)
include(cloud-storage.m4)
include(smart-upload.m4)
include(analytics.defn(`PLATFORM').m4)
include(mqtt.m4)
')
')

include(secret.m4)
ifelse(defn(`PLATFORM'),`VCAC-A',include(network.m4))
include(volume.m4)

