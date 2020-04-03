class Plugin(object):
    """PlasmaFX Plugin.

    A PlasmaFX plugin is responsible for the 4 lights on
    a single Plasma light board.

    """

    def __init__(self):
        """Initialise PlasmaFX: Base Plugin."""

    def get_values(self, num_pixels, delta):
        """Return colour values at time."""
        return