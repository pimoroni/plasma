import time
from random import choice, random, uniform

import machine

import plasma

"""
This example uses a PIR sensor to trigger some spooky effects.
We connected ours up to our QW/ST connector.
"""

# Set how many LEDs you have
NUM_LEDS = 50

BRIGHTNESS = 0.8

HUE = 0.8

# randomly pick a different colour every time an effect fires
RANDOM = True


def spooky_flash():
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, HUE, 1.0, BRIGHTNESS / 2)
    time.sleep(0.1)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, HUE, 1.0, 0.0)
    time.sleep(0.1)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, HUE, 1.0, BRIGHTNESS / 2)
    time.sleep(0.1)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, HUE, 1.0, 0.0)
    time.sleep(0.1)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, HUE, 1.0, BRIGHTNESS / 2)
    time.sleep(0.1)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, HUE, 1.0, 0.0)
    time.sleep(0.1)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, HUE, 1.0, BRIGHTNESS)
    time.sleep(3)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, HUE, 1.0, BRIGHTNESS / 2)
    time.sleep(0.1)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, HUE, 1.0, 0.0)
    time.sleep(0.1)
    # uncomment next line to increase tension
    # time.sleep(randrange(0, 15))


def fire():
    while pir.value() == 1:
        # fire effect! Random red/orange hue, full saturation, random brightness
        for i in range(NUM_LEDS):
            led_strip.set_hsv(i, uniform(0.0, 50 / 360), 1.0, random())
        time.sleep(0.1)


def all_on():
    while pir.value == 1:
        # light up a solid colour while movement is detected
        for i in range(NUM_LEDS):
            led_strip.set_hsv(i, HUE, 1.0, BRIGHTNESS)
        time.sleep(0.1)


# set up the hardware
# WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_RGB)

# the pin the signal line of our PIR sensor is connected to
# If you're using one of our qw/st > DuPont cables and a Plasma Stick the blue SDA wire is GP4 and the yellow SCL wire is GP5
# If you're lucky enough to have a Plasma 2350 W, the blue SDA wire is GP20 and the yellow SCL wire is GP21
pir = machine.Pin("GP5", machine.Pin.IN, machine.Pin.PULL_UP)

# Start updating the LED strip
led_strip.start()

while True:
    # on movement
    if pir.value() == 1:
        print("Movement detected!")
        # pick a random colour
        if RANDOM is True:
            HUE = random()

        # pick a random effect
        effects = [spooky_flash, fire, all_on]
        choice(effects)()

        # if you want a specific effect, comment the lines above and uncomment one of these:
        # spooky_flash()
        # fire()
        # all_on()

    else:
        for i in range(NUM_LEDS):
            led_strip.set_hsv(i, 1.0, 1.0, 0.0)
        time.sleep(0.1)
