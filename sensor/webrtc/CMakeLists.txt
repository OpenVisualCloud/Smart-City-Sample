set(service "smtc_sensor_webrtc")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_smtc_common)
