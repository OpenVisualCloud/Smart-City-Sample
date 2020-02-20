include(../../script/forloop.m4)
include(../../maintenance/db-init/sensor-info.m4)

version: "3.7"

services:

include(cloud-db.m4)
include(cloud-web.m4)
include(cloud-storage.m4)
forloop(`SCENARIOIDX',1,defn(`NSCENARIOS'),`
forloop(`OFFICEIDX',1,defn(`NOFFICES'),`
    include(office.m4)
    ifelse(index(defn(`OFFICE_LOCATION'),`,'),-1,,`
        include(camera.m4)
        include(office-db.m4)
        include(discovery.m4)
        include(alert.m4)
        include(where-indexing.m4)
        include(office-storage.m4)
        include(smart-upload.m4)
        include(analytics.defn(`PLATFORM').m4)
        include(mqtt.m4)
    ')
')')
include(secret.m4)
include(network.m4)
