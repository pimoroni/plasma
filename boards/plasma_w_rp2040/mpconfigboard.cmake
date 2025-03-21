# cmake file for Raspberry Pi Pico W
set(PICO_BOARD "pico_w")

# Board specific version of the frozen manifest
set(MICROPY_FROZEN_MANIFEST ${MICROPY_BOARD_DIR}/manifest.py)

set(MICROPY_C_HEAP_SIZE 4096)

# Links micropy_lib_lwip and sets MICROPY_PY_LWIP = 1
# Picked up and expanded upon in mpconfigboard.h
set(MICROPY_PY_LWIP ON)

# Links cyw43-driver and sets:
# MICROPY_PY_NETWORK_CYW43 = 1,
# MICROPY_PY_SOCKET_DEFAULT_TIMEOUT_MS = 30000
set(MICROPY_PY_NETWORK_CYW43 ON)

# Adds mpbthciport.c
# And sets:
# MICROPY_PY_BLUETOOTH = 1,
# MICROPY_PY_BLUETOOTH_USE_SYNC_EVENTS = 1,
# MICROPY_PY_BLUETOOTH_ENABLE_CENTRAL_MODE = 1
set(MICROPY_PY_BLUETOOTH ON)

# Links pico_btstack_hci_transport_cyw43
# And sets:
# MICROPY_BLUETOOTH_BTSTACK = 1,
# MICROPY_BLUETOOTH_BTSTACK_CONFIG_FILE =
set(MICROPY_BLUETOOTH_BTSTACK ON)

# Sets:
# CYW43_ENABLE_BLUETOOTH = 1,
# MICROPY_PY_BLUETOOTH_CYW43 = 1
set(MICROPY_PY_BLUETOOTH_CYW43 ON)

set(PIMORONI_UF2_MANIFEST ${CMAKE_CURRENT_LIST_DIR}/manifest.txt)
set(PIMORONI_UF2_DIR ${CMAKE_CURRENT_LIST_DIR}/../../examples)
include(${CMAKE_CURRENT_LIST_DIR}/../common.cmake)