"""Test Plasma WS281X initialisation."""
import mock


def test_apa102_setup(rpi_ws281x):
    """Test init succeeds and GPIO pins are setup."""
    from plasma.ws281x import PlasmaWS281X

    plasma = PlasmaWS281X(10)
    plasma.show()

    rpi_ws281x.PixelStrip.assert_called_once()


def test_apa102_parse_options(rpi_ws281x):
    from plasma.ws281x import PlasmaWS281X

    options = PlasmaWS281X.parse_options(["13", "WS2812", "1"])
    assert "gpio_pin" in options
    assert "strip_type" in options
    assert "channel" in options

    options = PlasmaWS281X.parse_options(["brightness=50", "freq_hz=800000"])
    assert "brightness" in options
    assert "freq_hz" in options
