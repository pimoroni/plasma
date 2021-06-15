"""Plasma multi device LED driver."""
import sys
import pathlib

__version__ = '1.0.0'


def auto(default=None):
    """Return a Plasma device instance.

    Will try to get arguments from command-line,
    otherwise falling back to supplied defaults.

    """
    descriptor = None

    if len(sys.argv) > 1:
        descriptor = sys.argv[1]
    elif default is not None:
        descriptor = default
    else:
        raise ValueError("get_device requires a descriptor")

    plasma, options = get_device(descriptor)

    return plasma(**options)


def get_device(descriptor=None):
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

        if output_type in ["GPIO", "APA102"]:
            from .apa102 import PlasmaAPA102
            return PlasmaAPA102, PlasmaAPA102.parse_options(output_options)
        if output_type in ["USB", "SERIAL"]:
            from .serial import PlasmaSerial
            return PlasmaSerial, PlasmaSerial.parse_options(output_options)
        if output_type == "WS281X":
            from .ws281x import PlasmaWS281X
            return PlasmaWS281X, PlasmaWS281X.parse_options(output_options)

    raise ValueError(f"Invalid descriptor: {descriptor}")
