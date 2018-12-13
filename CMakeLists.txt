
cmake_minimum_required (VERSION 2.8.12)
project (loot_api_python)
include(ExternalProject)

set(EXTERNAL_PROJECTS_PATH "${CMAKE_BINARY_DIR}/external/src")
make_directory(${EXTERNAL_PROJECTS_PATH})

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

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

set(PYBIND11_VERSION "2.2.4")
set(PYBIND11_URL "https://github.com/pybind/pybind11/archive/v${PYBIND11_VERSION}.tar.gz")
set(PYBIND11_DOWNLOAD_PATH "${EXTERNAL_PROJECTS_PATH}/pybind11-${PYBIND11_VERSION}.tar.gz")
set(PYBIND11_EXTRACTED_PATH "${EXTERNAL_PROJECTS_PATH}/pybind11-${PYBIND11_VERSION}")

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
    if (NOT "${CMAKE_GENERATOR}" MATCHES "(Win64|IA64)")
        set(LIBLOOT_URL "https://github.com/loot/libloot/releases/download/0.14.0/libloot-0.14.0-0-g2e074a4_dev-win32.7z")
    else()
        set(LIBLOOT_URL "https://github.com/loot/libloot/releases/download/0.14.0/libloot-0.14.0-0-g2e074a4_dev-win64.7z")
    endif()
else()
    set(LIBLOOT_URL "https://github.com/loot/libloot/releases/download/0.14.0/libloot.tar.xz")
endif()

ExternalProject_Add(libloot
                    PREFIX "external"
                    URL ${LIBLOOT_URL}
                    CONFIGURE_COMMAND ""
                    BUILD_COMMAND ""
                    INSTALL_COMMAND "")
ExternalProject_Get_Property(libloot SOURCE_DIR)
set(LIBLOOT_EXTRACTED_PATH ${SOURCE_DIR})

include_directories("${CMAKE_SOURCE_DIR}/src"
                    "${LIBLOOT_EXTRACTED_PATH}/include")
link_directories(${LIBLOOT_EXTRACTED_PATH})
set(LIBLOOT_STATIC_LIBRARY "${CMAKE_STATIC_LIBRARY_PREFIX}loot${CMAKE_STATIC_LIBRARY_SUFFIX}")
set(LIBLOOT_SHARED_LIBRARY "${CMAKE_SHARED_LIBRARY_PREFIX}loot${CMAKE_SHARED_LIBRARY_SUFFIX}")

#######################################
# Test Masterlist
#######################################

ExternalProject_Add(test-masterlist
                    PREFIX "external"
                    URL "https://github.com/loot/oblivion/archive/7f125ae4464224ff785111c7667c2cff85c896ec.zip"
                    CONFIGURE_COMMAND ""
                    BUILD_COMMAND ""
                    INSTALL_COMMAND "")

#######################################
# Python Module
#######################################

pybind11_add_module(loot_api  "${CMAKE_SOURCE_DIR}/src/main.cpp"
                              "${CMAKE_SOURCE_DIR}/src/convenience.cpp"
                              "${CMAKE_BINARY_DIR}/generated/wrapper_version.cpp")

add_dependencies(loot_api libloot test-masterlist)

if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    target_link_libraries(loot_api PRIVATE ${LIBLOOT_STATIC_LIBRARY})
else()
    target_link_libraries(loot_api PRIVATE ${LIBLOOT_SHARED_LIBRARY})
endif()

########################################
# Testing
########################################

find_package(PythonInterp REQUIRED)

# Copy the API binary to the build directory.
add_custom_command(TARGET loot_api POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${LIBLOOT_EXTRACTED_PATH}/${LIBLOOT_SHARED_LIBRARY}"
        "$<TARGET_FILE_DIR:loot_api>/${LIBLOOT_SHARED_LIBRARY}")

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
        CONFIGURATIONS Release RelWithDebInfo)

install(FILES "${LIBLOOT_EXTRACTED_PATH}/${LIBLOOT_SHARED_LIBRARY}"
        "${CMAKE_SOURCE_DIR}/docs/README.md"
        DESTINATION "."
        CONFIGURATIONS Release RelWithDebInfo)

IF (MSVC)
    install(FILES $<TARGET_PDB_FILE:loot_api>
            DESTINATION .
            OPTIONAL
            CONFIGURATIONS RelWithDebInfo
            RENAME loot_api_python.pdb)
ENDIF ()

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

    IF (DEFINED ENV{APPVEYOR_REPO_BRANCH})
        set(GIT_DESCRIBE_STRING "${GIT_DESCRIBE_STRING}_$ENV{APPVEYOR_REPO_BRANCH}")
    ELSEIF (DEFINED ENV{TRAVIS_BRANCH})
        set(GIT_DESCRIBE_STRING "${GIT_DESCRIBE_STRING}_$ENV{TRAVIS_BRANCH}")
    ENDIF()
ELSE()
    SET (GIT_DESCRIBE_STRING "unknown-version")
ENDIF ()

if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    set(CPACK_GENERATOR "7Z")
else()
    set(CPACK_GENERATOR "TXZ")
endif()

set(CPACK_PACKAGE_VERSION "${GIT_DESCRIBE_STRING}-python$ENV{PYTHON_VERSION}")
set(CPACK_PACKAGE_DIRECTORY "${CMAKE_BINARY_DIR}/package")

include(CPack)
