set(service "kubernetes")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")
add_dependencies(build_${service} build_sensor_info_m4)
add_dependencies(start_${service} build_sensor_info_m4 build_${service} sign_smtc_certificate)
add_dependencies(stop_${service} build_sensor_info_m4 build_${service})

# add cleanup files
file(GLOB m4files "${CMAKE_CURRENT_SOURCE_DIR}/*.yaml.m4")
foreach(m4file ${m4files})
    string(REPLACE ".yaml.m4" ".yaml" yamlfile "${m4file}")
    set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${yamlfile}")
endforeach(m4file)
