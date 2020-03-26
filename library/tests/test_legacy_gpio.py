"""Test Plasma GPIO (APA102 wrapper) initialisation."""
import mock


def test_legacy_gpio_setup(GPIO):
    """Test init succeeds and GPIO pins are setup."""
    from plasma.gpio import PlasmaGPIO
    plasma = PlasmaGPIO(10, gpio_data=10, gpio_clock=11)
    plasma.show()

    GPIO.setmode.assert_called_once_with(GPIO.BCM)
    GPIO.setup.assert_has_calls([
        mock.call(10, GPIO.OUT),
        mock.call(11, GPIO.OUT)
    ])


def test_legacy_gpio_parse_options():
    from plasma.gpio import PlasmaGPIO

    options = PlasmaGPIO.parse_options(["10", "11"])
    assert "gpio_data" in options
    assert "gpio_clock" in options

    options = PlasmaGPIO.parse_options(["gpio_data=10", "gpio_clock=11"])
    assert "gpio_data" in options
    assert "gpio_clock" in options
