// Board and hardware specific configuration
#define MICROPY_HW_FLASH_STORAGE_BYTES          (PICO_FLASH_SIZE_BYTES - (2 * 1024 * 1024))

// I2C0 (non-default)
#define MICROPY_HW_I2C0_SDA  (PLASMA2350_SDA_PIN)
#define MICROPY_HW_I2C0_SCL  (PLASMA2350_SCL_PIN)

// Set up networking.
#define MICROPY_PY_NETWORK_HOSTNAME_DEFAULT     "Plasma2350W"

#define MICROPY_HW_BOARD_NAME                   "Pimoroni Plasma 2350 (LTE + WiFi)"

// Enable WiFi & PPP
#define MICROPY_PY_NETWORK                      (1)
#define MICROPY_PY_NETWORK_PPP_LWIP             (1)

// CYW43 driver configuration.
#define CYW43_USE_SPI                           (1)
#define CYW43_LWIP                              (1)
#define CYW43_GPIO                              (1)
#define CYW43_SPI_PIO                           (1)

#ifndef CYW43_WL_GPIO_COUNT
#define CYW43_WL_GPIO_COUNT 3
#endif

#define MICROPY_HW_PIN_EXT_COUNT CYW43_WL_GPIO_COUNT

int mp_hal_is_pin_reserved(int n);
#define MICROPY_HW_PIN_RESERVED(i) mp_hal_is_pin_reserved(i)

// Defines for the Plasma MicroPython module default args
#define PLASMA_CLOCK_PIN PLASMA2350_CLK_PIN
#define PLASMA_DATA_PIN PLASMA2350_DATA_PIN