"""Test Plasma basic initialisation."""
import mock


def test_legacy_setup(GPIO):
    """Test init succeeds and GPIO pins are setup."""
    from plasma import legacy as plasma
    plasma.show()

    GPIO.setmode.assert_called_once_with(GPIO.BCM)
    GPIO.setup.assert_has_calls([
        mock.call(plasma.DAT, GPIO.OUT),
        mock.call(plasma.CLK, GPIO.OUT)
    ])
