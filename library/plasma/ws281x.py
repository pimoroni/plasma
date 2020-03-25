import time
from .core import Plasma


class PlasmaWS281X(Plasma):
    options = {
        "gpio_pin": int,
        "strip_type": str,
        "channel": int,
        "brightness": int,
        "freq_hz": int,
        "dma": int,
        "invert": bool
    }

    option_order = ("gpio_pin", "strip_type", "channel", "brightness", "freq_hz", "dma", "invert")

    def __init__(self, light_count, gpio_pin=13, strip_type='WS2812', channel=1, brightness=255, freq_hz=800000, dma=10, invert=False):
        from rpi_ws281x import PixelStrip, ws

        strip_types = {}
        for t in ws.__dict__:
            if '_STRIP' in t:
                k = t.replace('_STRIP', '')
                v = getattr(ws, t)
                strip_types[k] = v

        strip_type = strip_types[strip_type]
        self._strip = PixelStrip(light_count, gpio_pin, freq_hz, dma, invert, brightness, channel, strip_type)
        self._strip.begin()

        Plasma.__init__(self, light_count)

    def show(self):
        """Output the buffer."""
        for i in range(self._strip.numPixels()):
            r, g, b, brightness = self._pixels[i]
            self._strip.setPixelColorRGB(i, r, g, b)

        self._strip.show()
