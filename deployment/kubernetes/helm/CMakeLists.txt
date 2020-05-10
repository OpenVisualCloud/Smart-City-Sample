set(service "helm")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")

# add cleanup files
set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${CMAKE_CURRENT_SOURCE_DIR}/smtc/values.yaml")
