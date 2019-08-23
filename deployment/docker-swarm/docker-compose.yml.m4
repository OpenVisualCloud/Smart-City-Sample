include(../../script/forloop.m4)
include(location.m4)

version: "3.1"

services:

include(cloud.m4)

forloop(`office_idx',1,defn(`NOFFICES'),`dnl
define(`OFFICE_NAME',`office'defn(`office_idx'))dnl
define(`OFFICE_LOCATION',defn(`location_'defn(`OFFICE_NAME')))dnl
define(`CAMERA_NETWORK',192.168.defn(`office_idx').0/24)dnl
include(office.m4)
include(camera.m4)
')dnl

include(network.m4)
include(secret.m4)
