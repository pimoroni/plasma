import pytest


def test_fx_cycle(argv, GPIO):
    """Test that set_sequence supports the output of a PlasmaFX Sequence"""
    from plasma import auto
    from plasma.apa102 import PlasmaAPA102
    from plasmafx import Sequence
    from plasmafx.plugins import FXCycle

    sequence = Sequence(10)
    sequence.set_plugin(0, FXCycle())

    plasma = auto("APA102:14:15:pixel_count=10")

    plasma.set_sequence(sequence.get_pixels())

    assert isinstance(plasma, PlasmaAPA102)