"""Serial class for Plasma light devices over USB Serial/UART."""
from .core import Plasma
from serial import Serial


class PlasmaSerial(Plasma):
    """Serial class for Plasma light devices over USB Serial/UART."""

    name = "Serial"

    options = {
        'light_count': int,
        'pixels_per_light': int,
        "port": str
    }

    option_order = ("port", )

    def __init__(self, light_count=1, pixels_per_light=4, port='/dev/ttyAMA0', baudrate=115200):
        """Initialise Serial device.

        :param light_count: Number of logical lights (or LEDs if pixels_per_light == 1)
        :param pixels_per_light: Number of pixels (RGB) per logical light
        :param port: Serial port name/path
        :param baudrate: Serial baud rate

        """
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
