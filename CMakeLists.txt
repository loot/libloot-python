
cmake_minimum_required (VERSION 3.1)
project (libloot-python)
include(ExternalProject)

set(EXTERNAL_PROJECTS_PATH "${CMAKE_BINARY_DIR}/external/src")
make_directory(${EXTERNAL_PROJECTS_PATH})

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

##############################
# Get Build Revision
##############################

set(LIBLOOT_PY_VERSION_MAJOR 4)
set(LIBLOOT_PY_VERSION_MINOR 0)
set(LIBLOOT_PY_VERSION_PATCH 2)

find_package(Git)

IF (GIT_FOUND)
    execute_process(COMMAND ${GIT_EXECUTABLE} rev-parse --short HEAD
                  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
                  OUTPUT_VARIABLE GIT_COMMIT_STRING
                  OUTPUT_STRIP_TRAILING_WHITESPACE)
ELSE()
    SET (GIT_COMMIT_STRING "unknown")
ENDIF ()

message(STATUS "libloot-python version: ${LIBLOOT_PY_VERSION_MAJOR}.${LIBLOOT_PY_VERSION_MINOR}.${LIBLOOT_PY_VERSION_PATCH}")
message(STATUS "Git revision: ${GIT_COMMIT_STRING}")

# Write to file.
configure_file("${CMAKE_SOURCE_DIR}/src/wrapper_version.cpp.in" "${CMAKE_BINARY_DIR}/generated/wrapper_version.cpp" @ONLY)
configure_file("${CMAKE_SOURCE_DIR}/python/setup.py" "${CMAKE_BINARY_DIR}/generated/setup.py" @ONLY)

#######################################
# pybind11
#######################################

set(PYBIND11_VERSION "2.4.2")
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
# libloot
#######################################

if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    if (NOT "${CMAKE_GENERATOR_PLATFORM}" MATCHES "x64")
        set(LIBLOOT_URL "https://github.com/loot/libloot/releases/download/0.15.0/libloot-0.15.0-0-g629fdab_master-win32.7z")
    else()
        set(LIBLOOT_URL "https://github.com/loot/libloot/releases/download/0.15.0/libloot-0.15.0-0-g629fdab_master-win64.7z")
    endif()
else()
    set(LIBLOOT_URL "https://github.com/loot/libloot/releases/download/0.15.0/libloot.tar.xz")
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
# Python Module
#######################################

pybind11_add_module(libloot-python  "${CMAKE_SOURCE_DIR}/src/main.cpp"
                              "${CMAKE_SOURCE_DIR}/src/convenience.cpp"
                              "${CMAKE_BINARY_DIR}/generated/wrapper_version.cpp")

# Set the target output name to loot to follow common Python library naming
# conventions (no lib, no -python).
set_target_properties(libloot-python PROPERTIES OUTPUT_NAME loot)

add_dependencies(libloot-python libloot)

if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    target_link_libraries(libloot-python PRIVATE ${LIBLOOT_STATIC_LIBRARY})
else()
    target_link_libraries(libloot-python PRIVATE ${LIBLOOT_SHARED_LIBRARY})
endif()

########################################
# Testing
########################################

find_package(PythonInterp REQUIRED)

# Copy the libloot binary to the build directory.
add_custom_command(TARGET libloot-python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${LIBLOOT_EXTRACTED_PATH}/${LIBLOOT_SHARED_LIBRARY}"
        "$<TARGET_FILE_DIR:libloot-python>/${LIBLOOT_SHARED_LIBRARY}")

enable_testing()

add_test(NAME python
         WORKING_DIRECTORY $<TARGET_FILE_DIR:libloot-python>
         COMMAND "${PYTHON_EXECUTABLE}" ${CMAKE_SOURCE_DIR}/test/test.py)

########################################
# Install
########################################

install(TARGETS libloot-python
        DESTINATION "loot"
        CONFIGURATIONS Release RelWithDebInfo)

install(FILES "${LIBLOOT_EXTRACTED_PATH}/${LIBLOOT_SHARED_LIBRARY}"
        "${CMAKE_SOURCE_DIR}/python/loot/__init__.py"
        DESTINATION "loot"
        CONFIGURATIONS Release RelWithDebInfo)

install(FILES "${CMAKE_SOURCE_DIR}/docs/README.md"
        "${CMAKE_BINARY_DIR}/generated/setup.py"
        "${CMAKE_SOURCE_DIR}/LICENSE"
        DESTINATION "."
        CONFIGURATIONS Release RelWithDebInfo)

IF (MSVC)
    install(FILES $<TARGET_PDB_FILE:libloot-python>
            DESTINATION "loot"
            OPTIONAL
            CONFIGURATIONS RelWithDebInfo
            RENAME libloot-python.pdb)
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

    string(REPLACE "/" "-" GIT_DESCRIBE_STRING ${GIT_DESCRIBE_STRING})
ELSE()
    SET (GIT_DESCRIBE_STRING "unknown-version")
ENDIF ()

set(CPACK_GENERATOR "ZIP")
set(CPACK_PACKAGE_VERSION "${GIT_DESCRIBE_STRING}-python$ENV{PYTHON_VERSION}")
set(CPACK_PACKAGE_DIRECTORY "${CMAKE_BINARY_DIR}/package")

include(CPack)
