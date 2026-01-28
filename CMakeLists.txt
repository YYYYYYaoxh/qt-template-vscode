cmake_minimum_required(VERSION 3.20)

get_filename_component(PROJECT_DIR_NAME ${CMAKE_SOURCE_DIR} NAME)
project(${PROJECT_DIR_NAME} LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

qt_standard_project_setup()

# 默认使用项目名作为可执行文件名
set(APP_NAME "${PROJECT_NAME}" CACHE STRING "Application name")

# Resource files
set(RESOURCE_FILES
    resources/resources.qrc
)

# Windows resource file for icon
if(WIN32)
    list(APPEND RESOURCE_FILES resources/app_icon.rc)
endif()

add_executable(${APP_NAME}
    src/main.cpp
    ${RESOURCE_FILES}
)

target_link_libraries(${APP_NAME} PRIVATE Qt6::Widgets)

get_filename_component(QT6_PREFIX "${Qt6_DIR}/../../.." ABSOLUTE)
set(QT6_LIB_DIR "${QT6_PREFIX}/lib")

set_target_properties(${APP_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    BUILD_RPATH "${QT6_LIB_DIR}"
    INSTALL_RPATH "${QT6_LIB_DIR}"
)
