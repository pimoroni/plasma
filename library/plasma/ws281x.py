"""Class for Plasma light devices in the WS281X/SK6812 family."""
from .core import Plasma


class PlasmaWS281X(Plasma):
    """Class for Plasma light devices in the WS281X/SK6812 family."""

    name = "WS281X"

    options = {
        'pixel_count': int,
        "gpio_pin": int,
        "strip_type": str,
        "channel": int,
        "brightness": int,
        "freq_hz": int,
        "dma": int,
        "invert": bool
    }

    option_order = ("gpio_pin", "strip_type", "channel", "brightness", "freq_hz", "dma", "invert")

    def __init__(self, pixel_count=1, gpio_pin=13, strip_type='WS2812', channel=None, brightness=255, freq_hz=800000, dma=10, invert=False):
        """Initialise WS281X device.

        :param pixel_count: Number of individual RGB LEDs
        :param gpio_pin: BCM GPIO pin for output signal
        :param strip_type: Strip type: one of WS2812 or SK6812
        :param channel: LED channel (0 or 1, or None for automatic)
        :param brightness: Global WS281X LED brightness scale
        :param freq_hz: WS281X output signal frequency (usually 800khz)
        :param dma: DMA channel
        :param invert: Invert signals for NPN-transistor based level shifters

        """
        from rpi_ws281x import PixelStrip, ws

        strip_types = {}
        for t in ws.__dict__:
            if '_STRIP' in t:
                k = t.replace('_STRIP', '')
                v = getattr(ws, t)
                strip_types[k] = v

        strip_type = strip_types[strip_type]

        if channel is None:
            if gpio_pin in [13]:
                channel = 1
            elif gpio_pin in [12, 18]:
                channel = 0

        self._strip = PixelStrip(pixel_count, gpio_pin, freq_hz, dma, invert, brightness, channel, strip_type)
        self._strip.begin()

        Plasma.__init__(self, pixel_count)

    def show(self):
        """Output the buffer."""
        for i in range(self._strip.numPixels()):
            r, g, b, brightness = self._pixels[i]
            self._strip.setPixelColorRGB(i, r, g, b)

        self._strip.show()
