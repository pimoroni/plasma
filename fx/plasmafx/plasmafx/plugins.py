"""Plasma: Light FX Sequencer - Built-in plugins."""

import pkg_resources
from .core import Plugin


plasma_fx_plugins = {}

for entry_point in pkg_resources.iter_entry_points("plasmafx.effect_plugins"):
    effect_handle = entry_point.name
    plasma_fx_plugins[effect_handle] = entry_point.load()
    globals()[f"FX{effect_handle}"] = entry_point.load()


class Solid(Plugin):
    """PlasmaFX: Solid continuous light colour."""

    def __init__(self, pixel_count, r, g, b):
        """Initialise PlasmaFX: Solid.

        :param r, g, b: Amount of red, green and blue

        """
        Plugin.__init__(self, pixel_count)
        self.set_colour(r, g, b)

    def set_colour(self, r, g, b):
        """Set solid colour.

        :param r, g, b: Amount of red, green and blue

        """
        self.r = r
        self.g = g
        self.b = b

    def get_pixels(self, delta):
        """Return colour values at time."""
        for _ in range(self._pixel_count):
            yield (self.r, self.g, self.b)


class Pulse(Plugin):
    """PlasmaFX: Pulsing light colour."""

    def __init__(self, pixel_count, sequence, speed=1):
        """Initialise PlasmaFX: Pulse.

        :param sequence: List of colours to pulse through
        :param speed: Speed of effect

        """
        Plugin.__init__(self, pixel_count)
        self.sequence = sequence
        self.speed = speed

    def _colour(self, index, channel):
        return self.sequence[index][channel]

    def _blend(self, channel, first, second, blend):
        result = (self._colour(second, channel) - self._colour(first, channel)) * float(blend)
        result += self._colour(first, channel)
        return int(result)

    def get_pixels(self, delta):
        """Return colour values at time."""
        length = len(self.sequence)
        position = (delta % self.speed) / float(self.speed)
        colour = length * position
        blend = colour - int(colour)
        first_colour = int(colour) % length
        second_colour = (first_colour + 1) % length

        r = self._blend(0, first_colour, second_colour, blend)
        g = self._blend(1, first_colour, second_colour, blend)
        b = self._blend(2, first_colour, second_colour, blend)

        for _ in range(self._pixel_count):
            yield (r, g, b)


class Spin(Plugin):
    """PlasmaFX: Spinning light effect."""

    def __init__(self, pixel_count, sequence, speed=1):
        """Initialise PlasmaFX: Pulse.

        :param sequence: List of colours to spin through
        :param speed: Speed of effect

        """
        if len(sequence) > pixel_count:
            raise ValueError(f"Sequence should contain at most {pixel_count} items.")
        Plugin.__init__(self, pixel_count)
        self.sequence = sequence
        self.speed = speed

    def get_pixels(self, delta):
        """Return colour values at time."""
        offset = int(delta / self.speed)

        for x in range(self._pixel_count):
            x += offset
            x %= len(self.sequence)
            yield self.sequence[x]
