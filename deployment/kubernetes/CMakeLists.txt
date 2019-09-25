set(service "kubernetes")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")

add_custom_target(start_port_forward "${CMAKE_CURRENT_SOURCE_DIR}/port-forward.sh" start)
add_custom_target(stop_port_forward "${CMAKE_CURRENT_SOURCE_DIR}/port-forward.sh" stop)

