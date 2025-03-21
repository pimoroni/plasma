// Board and hardware specific configuration// Board and hardware specific configuration
#define MICROPY_HW_BOARD_NAME                   "Plasma 2040"

#define MICROPY_HW_FLASH_STORAGE_BYTES          (PICO_FLASH_SIZE_BYTES - (1024 * 1024))

// I2C0 (non-default)
#define MICROPY_HW_I2C0_SCL  (21)
#define MICROPY_HW_I2C0_SDA  (20)