cmake_minimum_required (VERSION 2.8)

Project(smart_city NONE)
add_custom_target(update)

if (NOT DEFINED PLATFORM)
    set(PLATFORM "Xeon")
endif()
if (NOT DEFINED SCENARIO)
    set(SCENARIO "traffic")
endif()
if (NOT DEFINED NOFFICES)
    set(NOFFICES "1")
endif()
if (NOT DEFINED NCAMERAS)
    set(NCAMERAS "5")
endif()
if (NOT DEFINED NSERVICES)
    set(NSERVICES "3")
endif()

file(GLOB dirs "deployment" "*")
list(REMOVE_DUPLICATES dirs)
foreach (dir ${dirs})
    if(EXISTS ${dir}/CMakeLists.txt)
        add_subdirectory(${dir})
    endif()
endforeach()

# legal message
execute_process(COMMAND printf "\nThis script will build third party components licensed under various open source licenses into your container images. The terms under which those components may be used and distributed can be found with the license document that is provided with those components. Please familiarize yourself with those terms to ensure your distribution of those components complies with the terms of those licenses.\n\n")

