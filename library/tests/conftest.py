"""Test configuration.

These allow the mocking of various Python modules
that might otherwise have runtime side-effects.
"""
import os
import sys
import mock
import pytest
import pathlib
import tempfile


@pytest.fixture(scope='function', autouse=True)
def cleanup_plasma():
    """This fixture removes all plasma modules from sys.modules.

    This ensures that each module is fully re-imported, along with
    the fixtures for serial, etc, for each test function.

    """

    yield None
    to_delete = []
    for module in sys.modules:
        if module.startswith('plasma'):
            to_delete.append(module)

    for module in to_delete:
        del sys.modules[module]


@pytest.fixture(scope='function', autouse=False)
def GPIO():
    """Mock RPi.GPIO module."""

    GPIO = mock.MagicMock()
    # Fudge for Python < 37 (possibly earlier)
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi'].GPIO = GPIO
    sys.modules['RPi.GPIO'] = GPIO
    yield GPIO
    del sys.modules['RPi']
    del sys.modules['RPi.GPIO']


@pytest.fixture(scope='function', autouse=False)
def serial():
    """Mock serial (pyserial) module."""

    serial = mock.MagicMock()
    sys.modules['serial'] = serial
    yield serial
    del sys.modules['serial']


@pytest.fixture(scope='function', autouse=False)
def rpi_ws281x():
    """Mock rpi_ws281x module."""

    rpi_ws281x = mock.MagicMock()
    # Fake the WS2812_STRIP constant that's loaded into the strip_types dict
    rpi_ws281x.ws.WS2812_STRIP = 0
    sys.modules['rpi_ws281x'] = rpi_ws281x
    yield rpi_ws281x
    del sys.modules['rpi_ws281x']


@pytest.fixture(scope='function', autouse=False)
def config_file():
    """Temporary config file."""
    file = tempfile.NamedTemporaryFile(delete=False)
    file.write(b"""pixels: 100
devices:
    WS281X:
        pixels: 30
        pixels_per_light: 1
        offset: 0
        gpio_pin: 1
        strip_type: WS2812
    APA102:
        pixels: 30
        pixels_per_light: 1
        offset: 30
        gpio_data: 10
        gpio_clock: 11
    SERIAL:
        pixels: 40
        pixels_per_light: 1
        offset: 60
        port: /dev/ttyAMA0
""")
    file.flush()
    yield pathlib.Path(file.name)
    file.close()


@pytest.fixture(scope='function', autouse=False)
def argv():
    """Replace sys.argv to avoid feeding Plasma auto the test args."""
    argv = sys.argv
    sys.argv = []
    yield
    sys.argv = argv


@pytest.fixture(scope='function', autouse=False)
def argv_valid():
    """Replace sys.argv to avoid feeding Plasma auto the test args."""
    argv = sys.argv
    sys.argv = ["", "APA102:14:15"]
    yield
    sys.argv = argv
