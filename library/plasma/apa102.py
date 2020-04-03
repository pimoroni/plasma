"""Plasma support for APA102 style pixels."""
import time
from .core import Plasma


class PlasmaAPA102(Plasma):
    """Plasma support for APA102 style pixels."""

    name = "APA102"

    options = {
        'light_count': int,
        'pixels_per_light': int,
        "gpio_data": int,
        "gpio_clock": int
    }

    option_order = ("gpio_data", "gpio_clock")

    def __init__(self, light_count=1, pixels_per_light=4, gpio_data=14, gpio_clock=15, gpio=None):
        """Initialise an APA102 device.

        :param light_count: Number of logical lights (or LEDs if pixels_per_light == 1)
        :param pixels_per_light: Number of pixels (RGB) per logical light
        :param gpio_data: BCM pin for data
        :param gpio_clock: BCM pin for clock
        :param gpio: Optional GPIO back-end, should be RPi.GPIO compatible

        """
        self._gpio = gpio
        if self._gpio is None:
            import RPi.GPIO as GPIO
            self._gpio = GPIO

        self._gpio_data = gpio_data
        self._gpio_clock = gpio_clock
        self._gpio_is_setup = False
        Plasma.__init__(self, light_count, pixels_per_light=pixels_per_light)

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
            brightness = int(brightness * 31) & 0x1f
            self._write_byte(0b11100000 | brightness)
            self._write_byte(b)
            self._write_byte(g)
            self._write_byte(r)

        self._eof()
