from plasmafx.core import Plugin
from colorsys import hsv_to_rgb

class Cycle(Plugin):
    def __init__(self, speed=1.0, spread=1.0, offset=0, saturation=1.0, value=1.0):
        Plugin.__init__(self)
        self._speed = float(speed)
        self._saturation = float(saturation)
        self._value = float(value)
        self._spread = spread / 360.0
        self._offset = offset / 360.0

    def get_values(self, num_pixels, delta):
        delta /= 10.0
        delta *= self._speed
        values = []
        for x in range(num_pixels):
            hue = delta + (self._spread / num_pixels * x) + self._offset
            r, g, b = hsv_to_rgb(hue, self._saturation, self._value)
            r, g, b = [int(c * 255) for c in (r, g, b)]
            values += [r, g, b]
        return values
