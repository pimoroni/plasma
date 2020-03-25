"""Test Plasma Serial initialisation."""
import mock


def test_serial_setup(serial):
    """Test init succeeds and GPIO pins are setup."""
    from plasma.serial import PlasmaSerial
    plasma = PlasmaSerial(10, port="/dev/ttyAMA0", baudrate=8000)
    plasma.show()

    serial.Serial.assert_called_once_with("/dev/ttyAMA0", baudrate=8000)


def test_serial_parse_options():
    from plasma.serial import PlasmaSerial

    options = PlasmaSerial.parse_options(["/dev/ttyAMA0"])
    assert "port" in options

    options = PlasmaSerial.parse_options(["port=/dev/ttyAMA0"])
    assert "port" in options
