import time
from .plugins import Solid


class Sequence(object):
    """PlasmaFX Sequence.

    A PlasmaFX sequence is responsible for a sequence of
    Plasma light groupings.

    LEDs can be grouped into "lights" such as the 4 on a Plasma PCB
    or the 12+ on an Adafruit NeoPixel ring.

    """

    def __init__(self, light_count, pixels_per_light=1):
        """Initialise PlasmaFX Sequence.

        :param light_count: Number of logical "lights" in the sequence
        :param pixels_per_light: Number of actual pixels in each light

        """
        self._pixels_per_light = pixels_per_light
        self._light_count = light_count
        self.elements = [Solid(0, 0, 0) for x in range(self._light_count)]

    def set_plugin(self, element_index, plugin):
        """Set plugin for light at index."""
        self.elements[element_index] = plugin

    def get_raw(self):
        """Return raw pixel values for current time."""
        delta = time.time()
        values = []
        for element in range(self._light_count):
            values += self.elements[element].get_values(self._pixels_per_light, delta)
        return values

    def get_leds(self):
        """Return RGB tuples for each LED in the sequence."""
        values = []
        raw_values = self.get_raw()
        for x in range(0, self._light_count * self._pixels_per_light * 3, 3):
            values.append(tuple(raw_values[x:x + 3]))
        return values
