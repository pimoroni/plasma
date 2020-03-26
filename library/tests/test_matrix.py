def test_setup_matrix(config_file, GPIO, rpi_ws281x, serial):
    from plasma.matrix import PlasmaMatrix
    plasma = PlasmaMatrix(config_file)
    assert plasma.get_pixel_count() == 100
    assert plasma.get_device_count() == 3

def test_show_matrix(config_file, GPIO, rpi_ws281x, serial):
    from plasma.matrix import PlasmaMatrix
    plasma = PlasmaMatrix(config_file)
    plasma.show()

    rpi_ws281x.PixelStrip.assert_called_once()
    rpi_ws281x.PixelStrip().show.assert_called_once()

    serial.Serial().write.assert_called_once()
