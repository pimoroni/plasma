#!/usr/bin/env python3

from plasma import auto
import plasmafx
from plasmafx import plugins
import time


FPS = 60
NUM_LIGHTS = 10
PIXELS_PER_LIGHT = 4

plasma = auto(default=f"GPIO:14:15:light_count={NUM_LIGHTS}:pixels_per_light={PIXELS_PER_LIGHT}")

sequence = plasmafx.Sequence(plasma.get_light_count(), plasma.get_pixels_per_light())

for x in range(plasma.get_light_count()):
    sequence.set_plugin(x, plugins.FXCycle(
        speed=2,
        spread=360.0 / plasma.get_light_count(),
        offset=360.0 / plasma.get_light_count() * x
    ))

sequence.set_plugin(0, plugins.Pulse([
	(0, 0, 0),
	(255, 0, 255)
]))

sequence.set_plugin(1, plugins.Pulse([
        (255, 0, 0),
        (0, 0, 255),
        (0, 0, 0)
], speed=0.5))

while True:
    values = sequence.get_leds()

    for index, rgb in enumerate(values):
        # print("Setting pixel: {} to {}:{}:{}".format(index, *rgb))
        plasma.set_pixel(index, *rgb)
    plasma.show()
    time.sleep(1.0 / FPS)
