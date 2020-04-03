"""Wrapper for deprecated PlasmaGPIO output device."""
from .apa102 import PlasmaAPA102


class PlasmaGPIO(PlasmaAPA102):
    pass
