"""Wrapper for deprecated PlasmaUSB output device."""
from .serial import PlasmaSerial


class PlasmaUSB(PlasmaSerial):
    pass
