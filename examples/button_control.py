import time

from pimoroni import Button

import plasma

"""
Use the buttons to set the colour and brightness of your LED strip.

Hold A to move the hue around the colour wheel.
Press Boot/User to step the brightness, wrapping back round to off.
"""

# Set how many LEDs you have
NUM_LEDS = 50

# How far the hue moves each time round the loop while A is held
HUE_SPEED = 0.005

# How many brightness steps to divide the range into
BRIGHTNESS_STEPS = 10

user_sw = Button("USER_SW", repeat_time=0)
button_a = Button("BUTTON_A", repeat_time=0)

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_RGB)

# start updating the LED strip
led_strip.start()

hue = 0.0
brightness_step = BRIGHTNESS_STEPS

while True:
    # raw() is held-down, read() is one shot per press
    if button_a.raw():
        hue = (hue + HUE_SPEED) % 1.0

    if user_sw.read():
        # counting in steps keeps the levels exact, where adding 0.1 would drift
        brightness_step = (brightness_step + 1) % (BRIGHTNESS_STEPS + 1)
        print(f"Brightness: {brightness_step} / {BRIGHTNESS_STEPS}")

    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, hue, 1.0, brightness_step / BRIGHTNESS_STEPS)

    time.sleep(0.02)
