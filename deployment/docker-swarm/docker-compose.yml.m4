include(../common/forloop.m4)
include(../common/location.m4)
define(`NCAMERAS',`5')
define(`NSERVICES',`3')

version: "3.1"

services:

include(cloud.m4)

forloop(`office_idx',1,defn(`NOFFICES'),`
define(`OFFICE_NAME',`office'defn(`office_idx'))
define(`OFFICE_LOCATION',defn(`location_'defn(`OFFICE_NAME')))
define(`CAMERA_NETWORK',192.168.defn(`office_idx').0/24)
include(office.m4)
include(camera.m4)
')

include(network.m4)
include(secret.m4)
