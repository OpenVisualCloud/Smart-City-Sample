
add_custom_target(tunnels ${CMAKE_CURRENT_SOURCE_DIR}/build.sh "${PLATFORM}" "${SCENARIO}" "${NOFFICES}" "${NCAMERAS}" "${NANALYTICS}" "${FRAMEWORK}" "${NETWORK}" "${REGISTRY}")

