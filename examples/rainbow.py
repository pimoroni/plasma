#!/usr/bin/env python3

import colorsys
import time
import sys


NUM_LIGHTS = 10


print("""rainbow.py - Display a rainbow on Plasma lights

Optionally supply a device descriptor to use Plasma USB Serial vs GPIO:

./rainbow.py SERIAL:/dev/ttyACM0

Or your own choice of GPIO pins (Data/Clock):

./rainbow.py GPIO:14:15

Press Ctrl+C to exit.

""")


if len(sys.argv) > 1:
    from plasma import get_device
    Plasma, args = get_device(sys.argv[1])
    plasma = Plasma(NUM_LIGHTS, **args)
else:
    from plasma.gpio import PlasmaGPIO
    plasma = PlasmaGPIO(NUM_LIGHTS, 14, 15)


spacing = 360.0 / 16.0
hue = 0

# plasma.set_clear_on_exit()

while True:
    hue = int(time.time() * 100) % 360
    for x in range(plasma.get_pixel_count()):
        offset = x * spacing
        h = ((hue + offset) % 360) / 360.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
        plasma.set_pixel(x, r, g, b)

    plasma.show()
    time.sleep(0.001)
