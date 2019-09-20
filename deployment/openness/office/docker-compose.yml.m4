include(../../common/forloop.m4)
include(../../common/location.m4)

version: "3.7"

services:

define(`OFFICE_NAME',`office'defn(`OFFICEIDX'))
ifdef(`location_'defn(`OFFICE_NAME'),`
define(`OFFICE_LOCATION',defn(`location_'defn(`OFFICE_NAME')))
define(`CAMERA_NETWORK',192.168.defn(`OFFICEIDX').0/24)
define(`TRANSPORT_PORT',eval(`9300+'defn(`OFFICEIDX')))
define(`WEBPROXY_PORT',eval(`18080+'defn(`OFFICEIDX')))
include(office.m4)
')

include(volume.m4)
