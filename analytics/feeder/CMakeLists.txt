set(service "smtc_va_feeder")
add_custom_target(va_xeon "${CMAKE_CURRENT_SOURCE_DIR}/build.sh" "xeon")
add_custom_target(va_vcac-a "${CMAKE_CURRENT_SOURCE_DIR}/build.sh" "vcac-a")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
