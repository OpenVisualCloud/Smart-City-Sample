
add_custom_target(tunnels ${CMAKE_CURRENT_SOURCE_DIR}/build.sh DEPENDS build_smtc_web_cloud build_smtc_storage_manager build_smtc_smart_upload)

