if(NOT DEFINED PIMORONI_PICO_PATH)
set(PIMORONI_PICO_PATH ${CMAKE_CURRENT_LIST_DIR}/../pimoroni-pico)
endif()
include(${PIMORONI_PICO_PATH}/pimoroni_pico_import.cmake)

include_directories(${CMAKE_CURRENT_LIST_DIR}/../../)
include_directories(${PIMORONI_PICO_PATH}/micropython)

# Drivers, etc
list(APPEND CMAKE_MODULE_PATH "${PIMORONI_PICO_PATH}")
# modules_py/modules_py
list(APPEND CMAKE_MODULE_PATH "${PIMORONI_PICO_PATH}/micropython")
# All regular modules
list(APPEND CMAKE_MODULE_PATH "${PIMORONI_PICO_PATH}/micropython/modules")

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Essential
include(pimoroni_i2c/micropython)
include(pimoroni_bus/micropython)

# Pico Graphics Essential
include(hershey_fonts/micropython)
include(bitmap_fonts/micropython)
include(picographics/micropython)

# Pico Graphics Extra
include(pngdec/micropython)
include(jpegdec/micropython)

# RP2350 boards take PicoVector v3 from picovector-micropython, rasterising on core1.
# RP2040 boards keep the in-tree v2, since v3 assumes the RP2350's FIFO interrupt and
# hardware float. This MicroPython has no no-scan allocator, so the plain one stands in.
# v3 draws QR codes itself through the same qrcodegen the qrcode module wraps, so that
# module is only built where v2 is.
if(PICO_RP2350)
    set(PV_DUAL_CORE ON)
    find_package(PICOVECTOR_MICROPYTHON CONFIG REQUIRED)
    target_compile_definitions(usermod_picovector INTERFACE m_malloc_no_scan=m_malloc)
else()
    include(picovector/micropython)
    include(qrcode/micropython/micropython)
endif()

# Sensors & Breakouts
include(micropython-common-breakouts)

# Utility
include(adcfft/micropython)

# LEDs & Matrices
include(plasma/micropython)

# Servos & Motors
include(pwm/micropython)
include(servo/micropython)
include(encoder/micropython)
include(motor/micropython)

# Still required for version.py
include(modules_py/modules_py)

# C++ Magic Memory
include(cppmem/micropython)

# Disable build-busting C++ exceptions
include(micropython-disable-exceptions)

# Must call `enable_ulab()` to enable
include(micropython-common-ulab)
enable_ulab()
