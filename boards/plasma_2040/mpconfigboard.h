// Board and hardware specific configuration// Board and hardware specific configuration
#define MICROPY_HW_BOARD_NAME                   "Plasma 2040"

#define MICROPY_HW_FLASH_STORAGE_BYTES          (PICO_FLASH_SIZE_BYTES - (1024 * 1024))

// I2C0 (non-default)
#define MICROPY_HW_I2C0_SCL                     (21)
#define MICROPY_HW_I2C0_SDA                     (20)

// There is no good SPI bus broken out on Plasma 2040
// So disable default pins and force the user to pick
#define MICROPY_HW_SPI_NO_DEFAULT_PINS          (1)

// Defines for the Plasma MicroPython module default args
#define PLASMA_CLOCK_PIN 14
#define PLASMA_DATA_PIN 15