import machine
from breakout_trackball import BreakoutTrackball

import plasma

"""
Drive your LED strip with a Trackball breakout.
https://shop.pimoroni.com/products/trackball-breakout

Up and down set how much of the strip is lit, left and right set the hue.
"""

# Set how many LEDs you have
NUM_LEDS = 50

# How far the ball has to move before it counts
SENSITIVITY = 1

# How much the hue moves per step
HUE_STEP = 0.02

# set up I2C
i2c = machine.I2C()

# set up the trackball breakout
trackball = BreakoutTrackball(i2c)

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_RGB)

# start updating the LED strip
led_strip.start()

lit = 0
hue = 0.0

while True:
    state = trackball.read()

    if state[BreakoutTrackball.UP] > SENSITIVITY:
        lit = min(NUM_LEDS, lit + 1)
    if state[BreakoutTrackball.DOWN] > SENSITIVITY:
        lit = max(0, lit - 1)

    if state[BreakoutTrackball.LEFT] > SENSITIVITY:
        hue += HUE_STEP
    if state[BreakoutTrackball.RIGHT] > SENSITIVITY:
        hue -= HUE_STEP
    # keep the hue in range, since set_hsv does not like negative values
    hue %= 1.0

    for i in range(lit):
        led_strip.set_hsv(i, hue, 1.0, 1.0)

    for i in range(lit, NUM_LEDS):
        led_strip.set_rgb(i, 0, 0, 0)
