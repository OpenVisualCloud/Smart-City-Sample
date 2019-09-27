set(service "kubernetes")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")
add_custom_target(expose_service "${CMAKE_CURRENT_SOURCE_DIR}/expose-svc.sh")
