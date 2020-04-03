import time
from .core import Plasma


class PlasmaAPA102(Plasma):
    name = "APA102"

    options = {
        "gpio_data": int,
        "gpio_clock": int
    }

    option_order = ("gpio_data", "gpio_clock")

    def __init__(self, light_count, pixels_per_light=4, gpio_data=14, gpio_clock=15, gpio=None):
        self._gpio = gpio
        if self._gpio is None:
            import RPi.GPIO as GPIO
            self._gpio = GPIO

        self._gpio_data = gpio_data
        self._gpio_clock = gpio_clock
        self._gpio_is_setup = False
        Plasma.__init__(self, light_count, pixels_per_light=pixels_per_light)

    def use_pins(self, gpio_data, gpio_clock):
        raise NotImplementedError

    def _write_byte(self, byte):
        for x in range(8):
            self._gpio.output(self._gpio_data, byte & 0b10000000)
            self._gpio.output(self._gpio_clock, 1)
            time.sleep(0.0000005)
            byte <<= 1
            self._gpio.output(self._gpio_clock, 0)
            time.sleep(0.0000005)

    def _eof(self):
        # Emit exactly enough clock pulses to latch the small dark die APA102s which are weird
        # for some reason it takes 36 clocks, the other IC takes just 4 (number of pixels/2)
        self._gpio.output(self._gpio_data, 0)
        for x in range(36):
            self._gpio.output(self._gpio_clock, 1)
            time.sleep(0.0000005)
            self._gpio.output(self._gpio_clock, 0)
            time.sleep(0.0000005)

    def _sof(self):
        self._gpio.output(self._gpio_data, 0)
        for x in range(32):
            self._gpio.output(self._gpio_clock, 1)
            time.sleep(0.0000005)
            self._gpio.output(self._gpio_clock, 0)
            time.sleep(0.0000005)

    def show(self):
        """Output the buffer."""
        if not self._gpio_is_setup:
            self._gpio.setmode(self._gpio.BCM)
            self._gpio.setwarnings(False)
            self._gpio.setup(self._gpio_data, self._gpio.OUT)
            self._gpio.setup(self._gpio_clock, self._gpio.OUT)
            self._gpio_is_setup = True

        self._sof()

        for pixel in self._pixels:
            r, g, b, brightness = pixel
            self._write_byte(0b11100000 | brightness)
            self._write_byte(b)
            self._write_byte(g)
            self._write_byte(r)

        self._eof()
