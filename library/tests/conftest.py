"""Test configuration.

These allow the mocking of various Python modules
that might otherwise have runtime side-effects.
"""
import sys
import mock
import pytest


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
    sys.modules['rpi_ws281x'] = rpi_ws281x
    yield rpi_ws281x
    del sys.modules['rpi_ws281x']

