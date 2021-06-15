#!/usr/bin/env python3

import sys
import time

from plasma import auto


NUM_PIXELS = 10 * 4  # Original Plasma light boards have 4 pixels per light


print(f"""rainbow.py - Display a solid colour on Plasma lights

Supply the colour values (0-255) on the command line:

{sys.argv[0]} 255 0 255

Optionally supply a device descriptor to use Plasma USB Serial vs GPIO:

{sys.argv[0]} SERIAL:/dev/ttyACM0:pixel_count=10 255 0 255

Or your own choice of GPIO pins (Data/Clock):

{sys.argv[0]} GPIO:14:15:pixel_count=10 255 0 255

Press Ctrl+C to exit.

""")

colour_offset = len(sys.argv) - 3


plasma = auto(default=f"GPIO:14:15:pixel_count={NUM_PIXELS}")
# plasma.set_clear_on_exit()

spacing = 360.0 / 16.0
hue = 0

while True:
    hue = int(time.time() * 100) % 360
    for x in range(plasma.get_pixel_count()):
        r, g, b = [int(x) for x in sys.argv[colour_offset:]]
        plasma.set_pixel(x, r, g, b)

    plasma.show()
    time.sleep(0.001)
