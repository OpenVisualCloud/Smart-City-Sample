set(service "kubernetes")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")
add_custom_target(port_forwarding "${CMAKE_CURRENT_SOURCE_DIR}/port-forward.sh")
