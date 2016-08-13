
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

set(LOOT_API_URL "https://bintray.com/wrinklyninja/loot/download_file?file_path=loot-api_0.9.2-30-ge40624c_c%2B%2B-api.7z")
set(LOOT_API_DOWNLOAD_PATH "${EXTERNAL_PROJECTS_PATH}/loot-api_0.9.2-30-ge40624c_c++-api.7z")
set(LOOT_API_EXTRACTED_PATH "${EXTERNAL_PROJECTS_PATH}/loot-api_0.9.2-30-ge40624c_c++-api")

if (NOT EXISTS ${LOOT_API_DOWNLOAD_PATH})
    file(DOWNLOAD ${LOOT_API_URL} ${LOOT_API_DOWNLOAD_PATH})
endif()

execute_process(COMMAND ${CMAKE_COMMAND} -E tar -xfJ ${LOOT_API_DOWNLOAD_PATH}
  WORKING_DIRECTORY ${EXTERNAL_PROJECTS_PATH}
  RESULT_VARIABLE result)

include_directories("${LOOT_API_EXTRACTED_PATH}/include")
link_directories(${LOOT_API_EXTRACTED_PATH})
set(LOOT_API_STATIC_LIBRARY "${CMAKE_STATIC_LIBRARY_PREFIX}loot_api${CMAKE_STATIC_LIBRARY_SUFFIX}")
set(LOOT_API_SHARED_LIBRARY "${CMAKE_SHARED_LIBRARY_PREFIX}loot_api${CMAKE_SHARED_LIBRARY_SUFFIX}")

#######################################
# Test Masterlist
#######################################

set(MASTERLIST_URL "https://github.com/loot/oblivion/archive/059fde4e976b70ec6bfcc583f1dcdc18aa598651.zip")
set(MASTERLIST_DOWNLOAD_PATH "${EXTERNAL_PROJECTS_PATH}/oblivion-059fde4e976b70ec6bfcc583f1dcdc18aa598651.zip")
set(MASTERLIST_EXTRACTED_PATH "${EXTERNAL_PROJECTS_PATH}/oblivion-059fde4e976b70ec6bfcc583f1dcdc18aa598651")

if (NOT EXISTS ${MASTERLIST_DOWNLOAD_PATH})
    file(DOWNLOAD ${MASTERLIST_URL} ${MASTERLIST_DOWNLOAD_PATH})
endif()

execute_process(COMMAND ${CMAKE_COMMAND} -E tar xfz ${MASTERLIST_DOWNLOAD_PATH}
  WORKING_DIRECTORY ${EXTERNAL_PROJECTS_PATH}
  RESULT_VARIABLE result)

#######################################
# Python Module
#######################################

pybind11_add_module(loot_api "${CMAKE_SOURCE_DIR}/src/main.cpp")

target_link_libraries(loot_api PRIVATE ${LOOT_API_STATIC_LIBRARY})

########################################
# Testing
########################################

find_package(PythonInterp REQUIRED)

# Copy the API binary to the build directory.
add_custom_command(TARGET loot_api POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${LOOT_API_EXTRACTED_PATH}/${LOOT_API_SHARED_LIBRARY}"
        "$<TARGET_FILE_DIR:loot_api>/${LOOT_API_SHARED_LIBRARY}")

# Copy the test masterlist to the build directory.
add_custom_command(TARGET loot_api POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${MASTERLIST_EXTRACTED_PATH}/masterlist.yaml"
        "$<TARGET_FILE_DIR:loot_api>/masterlist.yaml")

# Also copy the test Python script to the build directory.
add_custom_command(TARGET loot_api POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${CMAKE_SOURCE_DIR}/src/test.py"
        "$<TARGET_FILE_DIR:loot_api>/test.py")

enable_testing()
add_test(NAME test
         COMMAND ${PYTHON_EXECUTABLE} -m unittest test)

########################################
# Install
########################################

install(TARGETS loot_api
        DESTINATION bin
        CONFIGURATIONS Release)

install(FILES "${LOOT_API_EXTRACTED_PATH}/${LOOT_API_SHARED_LIBRARY}"
        DESTINATION bin
        CONFIGURATIONS Release)

########################################
# CPack
########################################

# Get version info using Git if available
find_package(Git)

IF (GIT_FOUND)
    execute_process(COMMAND ${GIT_EXECUTABLE} describe --tags --long --always
                  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
                  OUTPUT_VARIABLE GIT_DESCRIBE_STRING
                  OUTPUT_STRIP_TRAILING_WHITESPACE)

    IF (${GIT_DESCRIBE_STRING} MATCHES "HEAD")
        IF ($ENV{APPVEYOR_REPO_BRANCH})
          set(GIT_DESCRIBE_STRING $ENV{APPVEYOR_REPO_BRANCH})
        ENDIF()
    ENDIF()
ELSE()
    SET (GIT_DESCRIBE_STRING "unknown-version")
ENDIF ()

set(CPACK_GENERATOR "7Z")
set(CPACK_PACKAGE_VERSION ${GIT_DESCRIBE_STRING})
set(CPACK_PACKAGE_DIRECTORY "${CMAKE_BINARY_DIR}/package")

include(CPack)
