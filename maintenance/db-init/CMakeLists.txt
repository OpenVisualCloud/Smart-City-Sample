set(service "smtc_db_init")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_custom_target(build_sensor_info_m4 "${CMAKE_CURRENT_SOURCE_DIR}/mkm4.sh")
add_dependencies(build_${service} build_smtc_common build_sensor_info_m4)

