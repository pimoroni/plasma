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


def test_apa102_set_pixel(GPIO):
    """Test a pixel can be set."""
    from plasma.apa102 import PlasmaAPA102
    plasma = PlasmaAPA102(10, gpio_data=10, gpio_clock=11)
    plasma.set_pixel(0, 255, 0, 255)
    
    assert plasma.get_pixel(0) == (255, 0, 255, 1.0)


def test_apa102_set_all(GPIO):
    """Test a pixel can be set."""
    from plasma.apa102 import PlasmaAPA102
    plasma = PlasmaAPA102(10, gpio_data=10, gpio_clock=11)
    plasma.set_all(255, 0, 255)
    
    assert plasma.get_pixel(0) == (255, 0, 255, 1.0)


def test_apa102_clear(GPIO):
    """Test all pixels are cleared."""
    from plasma.apa102 import PlasmaAPA102
    plasma = PlasmaAPA102(10, gpio_data=10, gpio_clock=11)
    plasma.set_all(255, 0, 255)
    plasma.clear()
    
    assert plasma.get_pixel(0) == (0, 0, 0, 1.0)


def test_apa102_set_brightness(GPIO):
    """Test brightness is set."""
    from plasma.apa102 import PlasmaAPA102
    plasma = PlasmaAPA102(10, gpio_data=10, gpio_clock=11)
    plasma.set_all(255, 0, 255)
    plasma.set_brightness(0.5)

    assert plasma.get_pixel(0) == (255, 0, 255, 0.5)


def test_matrix_set_sequence_dict(config_file, GPIO, rpi_ws281x, serial):
    from plasma.apa102 import PlasmaAPA102
    plasma = PlasmaAPA102(10, gpio_data=10, gpio_clock=11)
    plasma.set_sequence({
        0: (255, 0, 0),
        2: (0, 255, 0),
        4: (0, 0, 255)
    })

    assert plasma.get_pixel(0) == (255, 0, 0, 1.0)
    assert plasma.get_pixel(2) == (0, 255, 0, 1.0)
    assert plasma.get_pixel(4) == (0, 0, 255, 1.0)


def test_matrix_set_sequence_list(config_file, GPIO, rpi_ws281x, serial):
    from plasma.apa102 import PlasmaAPA102
    plasma = PlasmaAPA102(10, gpio_data=10, gpio_clock=11)
    plasma.set_sequence([
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255)
    ])

    assert plasma.get_pixel(0) == (255, 0, 0, 1.0)
    assert plasma.get_pixel(1) == (0, 255, 0, 1.0)
    assert plasma.get_pixel(2) == (0, 0, 255, 1.0)


def test_apa102_parse_options():
    from plasma.apa102 import PlasmaAPA102

    options = PlasmaAPA102.parse_options(["10", "11"])
    assert "gpio_data" in options
    assert "gpio_clock" in options

    options = PlasmaAPA102.parse_options(["gpio_data=10", "gpio_clock=11"])
    assert "gpio_data" in options
    assert "gpio_clock" in options
