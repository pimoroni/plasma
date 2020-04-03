"""Serial class for Plasma light devices over USB Serial/UART."""
from .core import Plasma
from serial import Serial


class PlasmaSerial(Plasma):
    name = "Serial"

    options = {
        "port": str
    }

    option_order = ("port", )

    def __init__(self, light_count, pixels_per_light=4, port='/dev/ttyAMA0', baudrate=115200):
        self._serial_port = port
        self._serial = Serial(port, baudrate=baudrate)
        Plasma.__init__(self, light_count, pixels_per_light=pixels_per_light)

    def show(self):
        """Display current buffer on LEDs."""
        sof = b"LEDS"
        eof = b"\x00\x00\x00\xff"

        pixels = []
        for pixel in self._pixels:
            for channel in pixel:
                pixels += [channel]

        self._serial.write(sof + bytearray(pixels) + eof)
        self._serial.flush()
