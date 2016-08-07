
cmake_minimum_required (VERSION 2.8.12)
project (loot_api_python)
include(ExternalProject)

set(EXTERNAL_PROJECTS_PATH "${CMAKE_BINARY_DIR}/external/src")
make_directory(${EXTERNAL_PROJECTS_PATH})

#######################################
# pybind11
#######################################

set(PYBIND11_URL "https://github.com/pybind/pybind11/archive/v1.8.1.tar.gz")
set(PYBIND11_DOWNLOAD_PATH "${EXTERNAL_PROJECTS_PATH}/pybind11-1.8.1.tar.gz")
set(PYBIND11_EXTRACTED_PATH "${EXTERNAL_PROJECTS_PATH}/pybind11-1.8.1")

if (NOT EXISTS ${PYBIND11_DOWNLOAD_PATH})
    file(DOWNLOAD ${PYBIND11_URL} ${PYBIND11_DOWNLOAD_PATH})
endif()

execute_process(COMMAND ${CMAKE_COMMAND} -E tar xfz ${PYBIND11_DOWNLOAD_PATH}
  WORKING_DIRECTORY ${EXTERNAL_PROJECTS_PATH}
  RESULT_VARIABLE result)

add_subdirectory(${PYBIND11_EXTRACTED_PATH})

#######################################
# LOOT API
#######################################

set(LOOT_API_URL "https://bintray.com/wrinklyninja/loot/download_file?file_path=loot-api_0.9.2-20-g22d0577_api-archive-lib.7z")
set(LOOT_API_DOWNLOAD_PATH "${EXTERNAL_PROJECTS_PATH}/loot-api_0.9.2-20-g22d0577_api-archive-lib.7z")
set(LOOT_API_EXTRACTED_PATH "${EXTERNAL_PROJECTS_PATH}/loot-api_0.9.2-20-g22d0577_api-archive-lib")

if (NOT EXISTS ${LOOT_API_DOWNLOAD_PATH})
    file(DOWNLOAD ${LOOT_API_URL} ${LOOT_API_DOWNLOAD_PATH})
endif()

execute_process(COMMAND ${CMAKE_COMMAND} -E tar -xfJ ${LOOT_API_DOWNLOAD_PATH}
  WORKING_DIRECTORY ${EXTERNAL_PROJECTS_PATH}
  RESULT_VARIABLE result)

include_directories("${LOOT_API_EXTRACTED_PATH}/include")
link_directories(${LOOT_API_EXTRACTED_PATH})
set (LOOT_API_LIBRARIES "${CMAKE_STATIC_LIBRARY_PREFIX}loot_api${CMAKE_SHARED_LIBRARY_SUFFIX}")

#######################################
# Python Module
#######################################

pybind11_add_module(loot_api "${CMAKE_SOURCE_DIR}/src/main.cpp")

target_link_libraries(loot_api PRIVATE ${LOOT_API_LIBRARIES})

FOREACH(loot_api_library ${LOOT_API_LIBRARIES})
    add_custom_command(TARGET loot_api POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${LOOT_API_EXTRACTED_PATH}/${loot_api_library}
          $<TARGET_FILE_DIR:loot_api>/${loot_api_library})
ENDFOREACH()
