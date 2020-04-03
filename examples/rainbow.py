#!/usr/bin/env python3

import colorsys
import time

from plasma import auto


NUM_PIXELS = 10 * 4  # Original Plasma light boards have 4 pixels per light


print("""rainbow.py - Display a rainbow on Plasma lights

Optionally supply a device descriptor to use Plasma USB Serial vs GPIO:

./rainbow.py SERIAL:/dev/ttyACM0:pixel_count=10

Or your own choice of GPIO pins (Data/Clock):

./rainbow.py GPIO:14:15:pixel_count=10

Press Ctrl+C to exit.

""")

plasma = auto(default=f"GPIO:14:15:pixel_count={NUM_PIXELS}")
# plasma.set_clear_on_exit()

spacing = 360.0 / 16.0
hue = 0

while True:
    hue = int(time.time() * 100) % 360
    for x in range(plasma.get_pixel_count()):
        offset = x * spacing
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        plasma.set_pixel(x, r, g, b)

    plasma.show()
    time.sleep(0.001)
