include(../../../../script/loop.m4)

# platform specifies the target platform: Xeon or VCAC-A.
platform: "defn(`PLATFORM')"

# framework specifies the target framework: gst or ffmpeg.
framework: "defn(`FRAMEWORK')"

# scenario specifies the sample scenario(s) as a list: traffic or stadium. As each 
# scenario runs its own set of services and databases, it is recommended that you
# run multiple scenarios only on a multiple-node deployment.
scenario: 
looplist(`SCENARIO',defn(`SCENARIO'),`dnl
  - "defn(`SCENARIO')"
')dnl

# nOffices specifies the number of offices in the deployment. Support 1-3
# offices in the traffic scenario and 1 office in the stadium scenario.
nOffices: defn(`NOFFICES')

# nCameras specifies the number of cameras served in each office. Currently
# support 1-8 cameras. In stadium scenario, you can specify each camera numbers 
# as a list: <#entrance_counting>,<#crowd_counting>,<#service_queue_counting>,
# e.g. 5,1,3.
nCameras: 
looplist(`NCAMERA1',defn(`NCAMERAS'),`dnl
  - defn(`NCAMERA1')
')dnl

# nAnalytics specifies the number of analytics instances running in each office.
# In the stadium scenario, you can specify different analytics instances as a list
# for <#people_counting>,<#crowd_counting>,<#queue_counting>.
nAnalytics: 
looplist(`NANALYTICS1',defn(`NANALYTICS'),`dnl
  - defn(`NANALYTICS1')
')dnl

# cloudWebExternalIP specifies the external IP to access the Smart City or
# Stadium Sample web-cloud GUI
cloudWebExternalIP: "defn(`HOSTIP')"

# officeLocations provide simulated GPS coordinates for the Smart City & Stadium
# offices
officeLocations:
include(../../../../maintenance/db-init/sensor-info.m4)dnl
loop(SCENARIOIDX,1,defn(`NSCENARIOS'),`dnl
ifdef(`scenario'defn(`SCENARIOIDX'),`dnl
  defn(`scenario'defn(`SCENARIOIDX')):
loopifdef(OFFICEIDX,1,`defn(`scenario'defn(`SCENARIOIDX'))`_office'defn(`OFFICEIDX')`_location'',`dnl
  - "defn(defn(`scenario'defn(`SCENARIOIDX'))`_office'defn(`OFFICEIDX')`_location')"
')')')

# network specifies the analytics model precision: FP32, INT8 or FP16.
network_preference: "defn(`NETWORK_PREFERENCE')"

# default settings for IP camera simulation & discovery.
# IP cameras are assumed being deployed on 192.168.x.0/24 subnets.
discoverIPCamera: false
discoverSimulatedCamera: true
cameraRTSPPort: 17000
cameraRTPPort: 27000
cameraPortStep: 10

# optional: provide Linux user id & group permissioned to access cloud storage
# userID is obtained using command: `$ id -u`
# groupID is obtained using command: `$ id -g`
userID: defn(`USERID')
groupID: defn(`GROUPID')
