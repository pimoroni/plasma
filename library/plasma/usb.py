"""Wrapper around PlasmaSerial to provide deprecated PlasmaUSB output device."""
from .serial import PlasmaSerial


class PlasmaUSB(PlasmaSerial):
    """Deprecated PlasmaUSB output device."""

    pass
