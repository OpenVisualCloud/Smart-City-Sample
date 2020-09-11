set(service "helm")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")
add_dependencies(build_${service} build_sensor_info_m4)
add_dependencies(start_${service} build_sensor_info_m4 build_${service} sign_smtc_certificate)

# add cleanup files
set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${CMAKE_CURRENT_SOURCE_DIR}/smtc/values.yaml")
