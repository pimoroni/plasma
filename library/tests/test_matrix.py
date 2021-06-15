def test_matrix_setup(config_file, GPIO, rpi_ws281x, serial):
    from plasma.matrix import PlasmaMatrix
    plasma = PlasmaMatrix(config_file)
    assert plasma.get_pixel_count() == 100
    assert plasma.get_device_count() == 3


def test_matrix_set_pixel(config_file, GPIO, rpi_ws281x, serial):
    from plasma.matrix import PlasmaMatrix
    plasma = PlasmaMatrix(config_file)
    plasma.set_pixel(0, 255, 0, 0)   # First pixel of the WS281X
    plasma.set_pixel(30, 0, 255, 0)  # First pixel of the APA102
    plasma.set_pixel(60, 0, 0, 255)  # First pixel of the SERIAL

    assert plasma.get_device("WS281X").get_pixel(0) == (255, 0, 0, 1.0)
    assert plasma.get_device("APA102").get_pixel(0) == (0, 255, 0, 1.0)
    assert plasma.get_device("SERIAL").get_pixel(0) == (0, 0, 255, 1.0)


def test_matrix_get_pixel(config_file, GPIO, rpi_ws281x, serial):
    from plasma.matrix import PlasmaMatrix
    plasma = PlasmaMatrix(config_file)
    plasma.set_pixel(0, 255, 0, 0)   # First pixel of the WS281X
    plasma.set_pixel(30, 0, 255, 0)  # First pixel of the APA102
    plasma.set_pixel(60, 0, 0, 255)  # First pixel of the SERIAL

    assert plasma.get_pixel(0) == (255, 0, 0, 1.0)
    assert plasma.get_pixel(30) == (0, 255, 0, 1.0)
    assert plasma.get_pixel(60) == (0, 0, 255, 1.0)


def test_matrix_get_device(config_file, GPIO, rpi_ws281x, serial):
    from plasma.matrix import PlasmaMatrix
    plasma = PlasmaMatrix(config_file)
    plasma.set_pixel(0, 255, 0, 0)   # First pixel of the WS281X
    plasma.set_pixel(30, 0, 255, 0)  # First pixel of the APA102
    plasma.set_pixel(60, 0, 0, 255)  # First pixel of the SERIAL

    assert plasma.get_device("WS281X").get_pixel(0) == (255, 0, 0, 1.0)
    assert plasma.get_device("APA102").get_pixel(0) == (0, 255, 0, 1.0)
    assert plasma.get_device("SERIAL").get_pixel(0) == (0, 0, 255, 1.0)

    assert plasma.get_device("TABLE").get_pixel(0) == (255, 0, 0, 1.0)
    assert plasma.get_device("WALL").get_pixel(0) == (0, 255, 0, 1.0)
    assert plasma.get_device("BACKLIGHT").get_pixel(0) == (0, 0, 255, 1.0)


def test_matrix_show(config_file, GPIO, rpi_ws281x, serial):
    from plasma.matrix import PlasmaMatrix
    plasma = PlasmaMatrix(config_file)
    plasma.show()

    rpi_ws281x.PixelStrip.assert_called_once()
    rpi_ws281x.PixelStrip().show.assert_called_once()

    serial.Serial().write.assert_called_once()
