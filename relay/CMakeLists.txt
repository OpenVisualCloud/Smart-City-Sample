set(service "smtc_relay")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_smtc_common)
