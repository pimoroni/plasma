import time

import plasma

"""
Light the whole strip in one colour. A good first thing to try, and a good
way to check your LED count and colour order are right.
"""

# Set how many LEDs you have
NUM_LEDS = 50

# Set the colour, as red, green and blue values from 0 to 255
COLOUR = (100, 0, 100)

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_RGB)

# start updating the LED strip
led_strip.start()

for i in range(NUM_LEDS):
    led_strip.set_rgb(i, *COLOUR)

# the strip is refreshed in the background, so just keep the program alive
while True:
    time.sleep(1)
