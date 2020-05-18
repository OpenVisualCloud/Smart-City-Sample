if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build.sh")
    add_custom_target(build_${service} ALL "${CMAKE_CURRENT_SOURCE_DIR}/build.sh" "${PLATFORM}" "${SCENARIO}" "${NOFFICES}" "${NCAMERAS}" "${NANALYTICS}" "${FRAMEWORK}" "${NETWORK}" "${REGISTRY}")
endif()
