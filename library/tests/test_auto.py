import pytest


def test_auto_apa102(argv, GPIO):
    from plasma import auto
    from plasma.apa102 import PlasmaAPA102

    plasma = auto("APA102:14:15")

    assert isinstance(plasma, PlasmaAPA102)


def test_get_device_raises_valueerror(argv):
    from plasma import auto
    with pytest.raises(ValueError):
        auto()


def test_get_device_from_argv(argv_valid, GPIO):
    from plasma import auto
    from plasma.apa102 import PlasmaAPA102

    plasma = auto("XXXXX")

    assert isinstance(plasma, PlasmaAPA102)


def test_get_device_from_config(config_file, GPIO, rpi_ws281x, serial):
    from plasma import auto
    from plasma.matrix import PlasmaMatrix
    from plasma.apa102 import PlasmaAPA102

    plasma = auto("XXXXX", config_file)

    assert isinstance(plasma, PlasmaMatrix)
    assert isinstance(plasma.get_device("WALL"), PlasmaAPA102)

