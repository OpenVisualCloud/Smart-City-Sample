set(service "smtc_onvif_discovery")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_smtc_common)
add_custom_target(discover ${CMAKE_HOME_DIRECTORY}/sensor/discovery/shell.sh /home/discover.py $ENV{PORT_SCAN})
