"""Plasma: Light FX Sequencer."""
import time


class Sequence(object):
    """PlasmaFX Sequence.

    A PlasmaFX sequence is responsible for a sequence of
    Plasma light groupings.

    LEDs can be grouped into "lights" such as the 4 on a Plasma PCB
    or the 12+ on an Adafruit NeoPixel ring.

    """

    def __init__(self, pixel_count):
        """Initialise PlasmaFX Sequence.

        :param pixel_count: Number of individual pixels in sequence

        """
        self._pixel_count = pixel_count
        self._plugins = {}
        self._pixels = [(0, 0, 0) for _ in range(self._pixel_count)]

    def __iter__(self):
        self.update_pixels()

        for index, pixel in enumerate(self._pixels):
            yield index, pixel

    def set_plugin(self, offset, plugin):
        """Set plugin for light at index."""
        self._plugins[offset] = plugin

    def update_pixels(self, delta=None):
        if delta is None:
            delta = time.time()
        for offset, plugin in self._plugins.items():
            self._pixels[offset:offset + plugin.get_pixel_count()] = plugin.get_pixels(delta)

    def get_pixels(self, delta=None):
        """Return RGB tuples for each LED in sequence at current time.

        :param delta: Time value to use, (default: time.time())

        """
        self.update_pixels(delta)

        for index, pixel in enumerate(self._pixels):
            yield index, pixel
