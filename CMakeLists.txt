
cmake_minimum_required (VERSION 2.8.12)
project (loot_api_python)
include(ExternalProject)

set(EXTERNAL_PROJECTS_PATH "${CMAKE_BINARY_DIR}/external/src")
make_directory(${EXTERNAL_PROJECTS_PATH})

##############################
# Get Build Revision
##############################

find_package(Git)

IF (GIT_FOUND)
    execute_process(COMMAND ${GIT_EXECUTABLE} rev-parse --short HEAD
                  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
                  OUTPUT_VARIABLE GIT_COMMIT_STRING
                  OUTPUT_STRIP_TRAILING_WHITESPACE)
ELSE()
    SET (GIT_COMMIT_STRING "unknown")
ENDIF ()

message(STATUS "Git revision: ${GIT_COMMIT_STRING}")

# Write to file.
configure_file("${CMAKE_SOURCE_DIR}/src/wrapper_version.cpp.in" "${CMAKE_BINARY_DIR}/generated/wrapper_version.cpp" @ONLY)

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

if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    set(LOOT_API_URL "https://bintray.com/wrinklyninja/loot/download_file?file_path=loot-api_0.9.2-74-g6809c39_dev.7z")
else()
    set(LOOT_API_URL "https://bintray.com/wrinklyninja/loot/download_file?file_path=loot-api_0.9.2-74-g6809c39_dev.tar.xz")
endif()

ExternalProject_Add(loot-api-c++
                    PREFIX "external"
                    URL ${LOOT_API_URL}
                    CONFIGURE_COMMAND ""
                    BUILD_COMMAND ""
                    INSTALL_COMMAND "")
ExternalProject_Get_Property(loot-api-c++ SOURCE_DIR)
set(LOOT_API_EXTRACTED_PATH ${SOURCE_DIR})

include_directories("${CMAKE_SOURCE_DIR}/src"
                    "${LOOT_API_EXTRACTED_PATH}/include")
link_directories(${LOOT_API_EXTRACTED_PATH})
set(LOOT_API_STATIC_LIBRARY "${CMAKE_STATIC_LIBRARY_PREFIX}loot_api${CMAKE_STATIC_LIBRARY_SUFFIX}")
set(LOOT_API_SHARED_LIBRARY "${CMAKE_SHARED_LIBRARY_PREFIX}loot_api${CMAKE_SHARED_LIBRARY_SUFFIX}")

#######################################
# Test Masterlist
#######################################

ExternalProject_Add(test-masterlist
                    PREFIX "external"
                    URL "https://github.com/loot/oblivion/archive/059fde4e976b70ec6bfcc583f1dcdc18aa598651.zip"
                    CONFIGURE_COMMAND ""
                    BUILD_COMMAND ""
                    INSTALL_COMMAND "")

#######################################
# Python Module
#######################################

pybind11_add_module(loot_api "${CMAKE_SOURCE_DIR}/src/main.cpp" "${CMAKE_BINARY_DIR}/generated/wrapper_version.cpp")

add_dependencies(loot_api loot-api-c++ test-masterlist)

if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    target_link_libraries(loot_api PRIVATE ${LOOT_API_STATIC_LIBRARY})
else()
    target_link_libraries(loot_api PRIVATE ${LOOT_API_SHARED_LIBRARY})
endif()

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
ExternalProject_Get_Property(test-masterlist SOURCE_DIR)
add_custom_command(TARGET loot_api POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${SOURCE_DIR}/masterlist.yaml"
        "$<TARGET_FILE_DIR:loot_api>/masterlist.yaml")

# Also copy the test Python script to the build directory.
add_custom_command(TARGET loot_api POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${CMAKE_SOURCE_DIR}/src/test.py"
        "$<TARGET_FILE_DIR:loot_api>/test.py")

########################################
# Install
########################################

install(TARGETS loot_api
        DESTINATION "."
        CONFIGURATIONS Release)

install(FILES "${LOOT_API_EXTRACTED_PATH}/${LOOT_API_SHARED_LIBRARY}"
        "${CMAKE_SOURCE_DIR}/docs/README.md"
        DESTINATION "."
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

if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    set(CPACK_GENERATOR "7Z")
else()
    set(CPACK_GENERATOR "TXZ")
endif()

set(CPACK_PACKAGE_VERSION ${GIT_DESCRIBE_STRING})
set(CPACK_PACKAGE_DIRECTORY "${CMAKE_BINARY_DIR}/package")

include(CPack)
