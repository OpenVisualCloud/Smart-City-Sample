set(service "smtc_certificate")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${CMAKE_CURRENT_SOURCE_DIR}/self.crt" "${CMAKE_CURRENT_SOURCE_DIR}/self.key")
