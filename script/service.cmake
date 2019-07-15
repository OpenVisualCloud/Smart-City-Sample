if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build.sh")
    add_custom_target(build_${service} ALL "${CMAKE_CURRENT_SOURCE_DIR}/build.sh")
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/update.sh")
    add_custom_target(update_${service} "${CMAKE_CURRENT_SOURCE_DIR}/update.sh")
    add_dependencies(update update_${service})
endif()
