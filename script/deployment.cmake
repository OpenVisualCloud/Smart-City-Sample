add_custom_target(deploy_${service} "${CMAKE_CURRENT_SOURCE_DIR}/start.sh" "${service}")
add_custom_target(start_${service} "${CMAKE_CURRENT_SOURCE_DIR}/start.sh" "${service}")
add_custom_target(stop_${service} "${CMAKE_CURRENT_SOURCE_DIR}/stop.sh" "${service}")
