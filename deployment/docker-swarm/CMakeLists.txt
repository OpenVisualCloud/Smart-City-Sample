set(service "docker_swarm")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")

if (NOT PLATFORM STREQUAL "VCAC-A")
    set(service "docker_compose")
    include("${CMAKE_SOURCE_DIR}/script/service.cmake")
    include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")
endif()
