set(service "smtc_sensor_simulation")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")

# add stream to the clean list
execute_process(COMMAND cut -f2 -d, "${CMAKE_CURRENT_SOURCE_DIR}/streamlist.txt" OUTPUT_VARIABLE tmp)
string(REPLACE "\n" ";" streams ${tmp})
foreach(s ${streams})
    set_property(DIRECTORY APPEND PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "${CMAKE_CURRENT_SOURCE_DIR}/${s}") 
endforeach(s)
