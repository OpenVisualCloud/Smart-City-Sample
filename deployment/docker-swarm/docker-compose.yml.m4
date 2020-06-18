include(../../script/loop.m4)
include(../../maintenance/db-init/sensor-info.m4)

version: "3.7"

services:

include(cloud-db.m4)
include(cloud-web.m4)
include(cloud-storage.m4)
looplist(SCENARIO_NAME,defn(`SCENARIOS'),`
loop(`OFFICEIDX',1,defn(`NOFFICES'),`
    include(office.m4)
    ifelse(len(defn(`OFFICE_LOCATION')),0,,`
        include(camera.m4)
        include(office-db.m4)
        include(discovery.m4)
        include(alert.m4)
        include(office-storage.m4)
        include(smart-upload.m4)
        include(analytics.m4)
        include(mqtt.m4)
        include(mqtt2db.m4)
    ')
')')
include(secret.m4)
include(network.m4)
