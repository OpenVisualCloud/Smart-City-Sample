define(`OFFICE_NAME',defn(`SCENARIO_NAME')`_office'defn(`OFFICEIDX'))dnl
define(`OFFICE_LOCATION',ifelse(index(defn(`SCENARIO'),defn(`SCENARIO_NAME')),-1,,`defn(defn(`SCENARIO_NAME')`_office'defn(`OFFICEIDX')_location)'))dnl
define(`CAMERA_RTSP_PORT',17000)dnl
define(`CAMERA_RTP_PORT',27000)dnl
define(`CAMERA_PORT_STEP',10)dnl
define(`DISCOVER_IP_CAMERA',`false')dnl
define(`IP_CAMERA_NETWORK',192.168.defn(`OFFICEIDX').0/24)dnl
define(`DISCOVER_SIMULATED_CAMERA',`true')dnl
