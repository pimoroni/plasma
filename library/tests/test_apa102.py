"""Test Plasma APA102 initialisation."""
import mock


def test_apa102_setup(GPIO):
    """Test init succeeds and GPIO pins are setup."""
    from plasma.apa102 import PlasmaAPA102
    plasma = PlasmaAPA102(10, gpio_data=10, gpio_clock=11)
    plasma.show()

    GPIO.setmode.assert_called_once_with(GPIO.BCM)
    GPIO.setup.assert_has_calls([
        mock.call(10, GPIO.OUT),
        mock.call(11, GPIO.OUT)
    ])


def test_apa102_parse_options():
    from plasma.apa102 import PlasmaAPA102

    options = PlasmaAPA102.parse_options(["10", "11"])
    assert "gpio_data" in options
    assert "gpio_clock" in options

    options = PlasmaAPA102.parse_options(["gpio_data=10", "gpio_clock=11"])
    assert "gpio_data" in options
    assert "gpio_clock" in options
