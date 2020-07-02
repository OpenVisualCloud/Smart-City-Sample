set(service "smtc_sensor_simulation")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${CMAKE_CURRENT_SOURCE_DIR}/archive")
add_dependencies(build_${service} build_smtc_common)
