include(../common/forloop.m4)
include(../common/location.m4)

version: "3.7"

services:

include(cloud.m4)

forloop(`id',1,defn(`NOFFICES'),`
define(`OFFICE_NAME',`office'defn(`id'))
ifdef(`location_'defn(`OFFICE_NAME'),`
define(`OFFICE_LOCATION',defn(`location_'defn(`OFFICE_NAME')))
define(`CAMERA_NETWORK',192.168.defn(`id').0/24)
include(office.m4)
include(analytics.defn(`PLATFORM').m4)
include(camera.m4)
')
')

include(secret.m4)
