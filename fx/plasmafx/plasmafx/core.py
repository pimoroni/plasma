"""Plasma: Light FX Sequencer - Plugin base class."""


class Plugin(object):
    """PlasmaFX Plugin.

    A PlasmaFX plugin is responsible for the 4 lights on
    a single Plasma light board.

    """

    def __init__(self, pixel_count=1):
        """Initialise PlasmaFX: Base Plugin."""
        self._pixel_count = pixel_count

    def get_pixels(self, delta):
        """Return RGB tuples for each LED in sequence at current time."""
        for _ in range(self._pixel_count):
            yield (0, 0, 0)

    def get_pixel_count(self):
        """Return count of plugin managed pixels."""
        return self._pixel_count
