import pkg_resources
from .core import Plugin


plasma_fx_plugins = {}

for entry_point in pkg_resources.iter_entry_points("plasmafx.effect_plugins"):
    effect_handle = entry_point.name
    plasma_fx_plugins[effect_handle] = entry_point.load()
    globals()[f"FX{effect_handle}"] = entry_point.load()


class Solid(Plugin):
    """PlasmaFX: Solid continuous light colour."""

    def __init__(self, r, g, b, pixels_per_light=1):
        """Initialise PlasmaFX: Solid.

        :param r, g, b: Amount of red, green and blue

        """
        Plugin.__init__(self)
        self.set_colour(r, g, b)

    def set_colour(self, r, g, b):
        """Set solid colour.

        :param r, g, b: Amount of red, green and blue

        """
        self.r = r
        self.g = g
        self.b = b

    def get_values(self, num_pixels, delta):
        """Return colour values at time."""
        return [self.r, self.g, self.b] * num_pixels


class Pulse(Plugin):
    """PlasmaFX: Pulsing light colour."""

    def __init__(self, sequence, speed=1):
        """Initialise PlasmaFX: Pulse.

        :param sequence: List of colours to pulse through
        :param speed: Speed of effect

        """
        Plugin.__init__(self)
        self.sequence = sequence
        self.speed = speed

    def _colour(self, index, channel):
        return self.sequence[index][channel]

    def _blend(self, channel, first, second, blend):
        result = (self._colour(second, channel) - self._colour(first, channel)) * float(blend)
        result += self._colour(first, channel)
        return int(result)

    def get_values(self, num_pixels, delta):
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

        return [r, g, b] * num_pixels
