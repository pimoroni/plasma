"""Base class for Plasma LED devices."""
import atexit


class Plasma():
    """Base class for Plasma LED devices."""

    name = ""

    options = {
        'pixel_count': int,
    }

    option_order = []

    def __init__(self, pixel_count=1):
        """Initialise Plasma device.

        :param pixel_count: Number of individual RGB LEDs

        """
        self._pixel_count = pixel_count
        self._pixels = [[0, 0, 0, 1.0]] * self._pixel_count
        self._clear_on_exit = False

        atexit.register(self.atexit)

    @classmethod
    def parse_options(self, options):
        """Parse option string into kwargs dict."""
        named_options = {}
        for index, option in enumerate(options):
            if "=" in option:
                k, v = option.split("=")
            else:
                v = option
                k = self.option_order[index]
            named_options[k] = self.options[k](v)

        return named_options

    def get_pixel_count(self):
        """Get the count of pixels."""
        return self._pixel_count

    def show(self):
        """Display changes."""
        raise NotImplementedError

    def atexit(self):
        """Clear the display upon exit."""
        if not self._clear_on_exit:
            return
        self.clear()
        self.show()

    def set_pixel_hsv(self, index, h, s, v):
        """Set the HSV colour of an individual pixel in your chain."""
        raise NotImplementedError

    def set_clear_on_exit(self, status=True):
        """Set if the pixel strip should be cleared upon program exit."""
        self._clear_on_exit = status

    def set_all(self, r, g, b, brightness=None):
        """Set the RGB value and optionally brightness of all pixels.

        If you don't supply a brightness value, the last value set for each pixel be kept.

        :param r: Amount of red: 0 to 255
        :param g: Amount of green: 0 to 255
        :param b: Amount of blue: 0 to 255
        :param brightness: Brightness: 0.0 to 1.0 (default is 1.0)

        """
        for x in range(self._pixel_count):
            self.set_pixel(x, r, g, b, brightness)

    def get_pixel(self, x):
        """Get the RGB and brightness value of a specific pixel.

        :param x: The horizontal position of the pixel: 0 to 7

        """
        r, g, b, brightness = self._pixels[x]

        return r, g, b, brightness

    def set_pixel(self, x, r, g, b, brightness=None):
        """Set the RGB value, and optionally brightness, of a single pixel.

        If you don't supply a brightness value, the last value will be kept.

        :param x: The horizontal position of the pixel: 0 to 7
        :param r: Amount of red: 0 to 255
        :param g: Amount of green: 0 to 255
        :param b: Amount of blue: 0 to 255
        :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)

        """
        r, g, b = [int(c) & 0xff for c in (r, g, b)]

        if brightness is None:
            brightness = self._pixels[x][3]

        self._pixels[x] = [r, g, b, brightness]

    def clear(self):
        """Clear the pixel buffer."""
        for x in range(self._pixel_count):
            self._pixels[x][0:3] = [0, 0, 0]

    def set_brightness(self, brightness):
        """Set the brightness of all pixels.

        :param brightness: Brightness: 0.0 to 1.0

        """
        if brightness < 0 or brightness > 1:
            raise ValueError('Brightness should be between 0.0 and 1.0')

        for x in range(self._pixel_count):
            self._pixels[x][3] = brightness
