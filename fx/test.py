#!/usr/bin/env python3

from plasma import auto
import plasmafx
from plasmafx import plugins
import time


FPS = 60
PIXEL_COUNT = 10
PIXELS_PER_LIGHT = 4


print("""Plasma FX Plugin Test.

This test is designed for the original Plasma Light boards.

Each light has 4 pixels, so we set up a sequence of plugins that each handle 4 pixels.

Now we can flash or cycle individual lights.

""")

plasma = auto(default=f"GPIO:14:15:pixel_count={PIXEL_COUNT}")

sequence = plasmafx.Sequence(plasma.get_pixel_count())

light_count = plasma.get_pixel_count() // PIXELS_PER_LIGHT

for x in range(light_count - 1):
    sequence.set_plugin(x * PIXELS_PER_LIGHT, plugins.FXCycle(
        light_count,
        speed=2,
        spread=360.0 / light_count,
        offset=360.0 / light_count * x
    ))

sequence.set_plugin(0 * PIXELS_PER_LIGHT, plugins.Pulse(
    light_count, [
	(0, 0, 0),
	(255, 0, 255)]
))

sequence.set_plugin(1 * PIXELS_PER_LIGHT, plugins.Pulse(
        light_count, [
        (255, 0, 0),
        (0, 0, 255),
        (0, 0, 0)],
speed=0.5))

sequence.set_plugin(2 * PIXELS_PER_LIGHT, plugins.Spin(
    light_count, [
        (255, 255, 0),
        (0, 0, 255)
    ],
speed=0.1))

try:
    while True:
        plasma.set_sequence(sequence)
        plasma.show()
        time.sleep(1.0 / FPS)

except KeyboardInterrupt:
    plasma.set_all(0, 0, 0)
    plasma.show()
