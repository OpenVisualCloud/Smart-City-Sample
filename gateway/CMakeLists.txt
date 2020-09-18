set(service "smtc_api_gateway")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_smtc_common)
