set(service "smtc_analytics_object_detection")
set(build_options ${PLATFORM})
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_smtc_analytics_common)
