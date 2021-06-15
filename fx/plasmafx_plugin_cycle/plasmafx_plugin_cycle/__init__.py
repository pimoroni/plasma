"""Plasma: Light FX Sequencer - Colour Cycling Plugin."""
from plasmafx.core import Plugin
from colorsys import hsv_to_rgb


class Cycle(Plugin):
    """Plasma: Light FX Sequencer - Colour Cycling Plugin."""

    def __init__(self, pixel_count=1, speed=1.0, spread=360.0, offset=0.0, saturation=1.0, value=1.0):
        """Initialise PlasmaFX: Cycle.

        :param speed: Speed of cycling effect
        :param spread: Spread of effect around HSV circumference in degrees
        :param offset: Offset in degrees
        :param saturation: Colour saturation
        :param value: Colour value (effectively brightness)

        """
        Plugin.__init__(self, pixel_count)
        self._speed = float(speed)
        self._saturation = float(saturation)
        self._value = float(value)
        self._spread = spread / 360.0
        self._offset = offset / 360.0
        self._pixel_separation = self._spread / self._pixel_count

    def get_pixels(self, delta):
        """Return colour values at time."""
        delta /= 10.0
        delta *= self._speed
        for x in range(self._pixel_count):
            hue = delta + (self._pixel_separation * x) + self._offset
            r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, self._saturation, self._value)]
            yield (r, g, b)
