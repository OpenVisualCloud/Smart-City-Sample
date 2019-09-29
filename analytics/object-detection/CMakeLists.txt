set(service "smtc_analytics_object_detection")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_smtc_analytics_common build_smtc_common)
