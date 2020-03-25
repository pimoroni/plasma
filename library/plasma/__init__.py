import pathlib

__version__ = '1.0.0'


def get_device(descriptor):
    """Return a Plasma device class and arguments.

    :param descriptor: String describing device and arguments.

    This function accepts descriptors in the form:

    DEVICE:arg:arg

    IE: A serial connection would be described as:

    SERIAL:/dev/ttyACM0

    And GPIO as:

    GPIO:14:15

    And WS281X pixels as:

    WS281X:WS2812_RGB:13:1

    Additional optional arguments can be supplied by name, eg:

    WS281X:WS2812_RGB:13:1:freq_hz=800000

    """

    path = pathlib.Path(descriptor)
    if path.is_file():
        from .matrix import PlasmaMatrix
        return PlasmaMatrix, {'config_file': path}

    if type(descriptor) is str:
        dsc = descriptor.split(":")

        output_type = dsc[0]
        output_options = dsc[1:]

        if output_type == "GPIO":
            from .gpio import PlasmaGPIO
            return PlasmaGPIO, PlasmaGPIO.parse_options(output_options)
        if output_type == "SERIAL":
            from .usb import PlasmaSerial
            return PlasmaSerial, PlasmaSerial.parse_options(output_options)
        if output_type == "WS281X":
            from .ws281x import PlasmaWS281X
            return PlasmaWS281X, PlasmaWS281X.parse_options(output_options)
