set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_SYSTEM_PROCESSOR x86_64)

set(MXE_DIR "$ENV{MXE_DIR}")
if(NOT MXE_DIR)
    message(FATAL_ERROR "MXE_DIR is not set. Example: export MXE_DIR=/home/yxh/mxe")
endif()

set(MXE_TARGET "$ENV{MXE_TARGET}")
if(NOT MXE_TARGET)
    set(MXE_TARGET "x86_64-w64-mingw32.shared")
endif()

set(_mxe_conf "${MXE_DIR}/usr/${MXE_TARGET}/share/cmake/mxe-conf.cmake")
if(NOT EXISTS "${_mxe_conf}")
    message(FATAL_ERROR "MXE toolchain file not found: ${_mxe_conf}. Check MXE_DIR/MXE_TARGET.")
endif()

include("${_mxe_conf}")
