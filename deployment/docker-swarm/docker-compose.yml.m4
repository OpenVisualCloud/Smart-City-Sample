include(../../script/forloop.m4)

version: '3.1'

services:

include(cloud.m4)

define(`OFFICE_NAME',office1)dnl
define(`OFFICE_LOCATION',`45.539664,-122.937729')dnl
define(`CAMERA_NETWORK',192.168.1.0/24)dnl
include(office.m4)
include(camera.m4)

ifelse(eval(defn(`NOFFICES')>1),1,`dnl
define(`OFFICE_NAME',office2)dnl
define(`OFFICE_LOCATION',`45.548651,-122.965623')dnl
define(`CAMERA_NETWORK',192.168.2.0/24)dnl
include(office.m4)
include(camera.m4)
')dnl

ifelse(eval(defn(`NOFFICES')>2),1,`dnl
define(`OFFICE_NAME',office3)dnl
define(`OFFICE_LOCATION',`45.540001,-122.993239')dnl
define(`CAMERA_NETWORK',192.168.3.0/24)dnl
include(office.m4)
include(camera.m4)
')dnl

include(network.m4)
include(secret.m4)
