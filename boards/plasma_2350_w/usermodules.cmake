list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../")

# RGBA4444 canvases, half the bytes of RGBA8888, so a full 2.8" canvas fits beside the
# heap on a board with SRAM alone. picovector and the screen driver both read this, and
# it has to be set before either is found.
set(PV_PIXEL_FORMAT 2)

include(usermod-common)

# SP/CE screens on the connector. The GC heap owns this board's SRAM, so the displays'
# region is a block of it sized for two.
set(SPIDISPLAY_HEAP_RESERVE_BYTES 16384)
find_package(SPIDISPLAY CONFIG REQUIRED)