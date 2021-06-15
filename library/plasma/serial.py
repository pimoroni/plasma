"""Serial class for Plasma light devices over USB Serial/UART."""
from .core import Plasma
from serial import Serial


class PlasmaSerial(Plasma):
    """Serial class for Plasma light devices over USB Serial/UART."""

    name = "Serial"

    options = {
        'pixel_count': int,
        "port": str
    }

    option_order = ("port", )

    def __init__(self, pixel_count=1, port='/dev/ttyAMA0', baudrate=115200):
        """Initialise Serial device.

        :param pixel_count: Number of individual RGB LEDs
        :param port: Serial port name/path
        :param baudrate: Serial baud rate

        """
        self._serial_port = port
        self._serial = Serial(port, baudrate=baudrate)
        Plasma.__init__(self, pixel_count)

    def show(self):
        """Display current buffer on LEDs."""
        sof = b"LEDS"
        eof = b"\x00\x00\x00\xff"

        pixels = []
        for pixel in self._pixels:
            r, g, b, brightness = pixel
            pixels += [r, g, b, int(brightness * 254)]

        self._serial.write(sof + bytearray(pixels) + eof)
        self._serial.flush()
