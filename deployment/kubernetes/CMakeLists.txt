set(service "kubernetes")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")
add_custom_target(port_forward "${CMAKE_CURRENT_SOURCE_DIR}/port-forward.sh")
