import math
import time

import machine
from breakout_encoder_wheel import CENTRE, BreakoutEncoderWheel
from pimoroni import RGBLED

import plasma

"""
Control pulsing LED patterns with an Encoder Wheel.

Pressing the middle button will change between Hue, Spread, Brightness and Speed mode.

Rotating the wheel will adjust the selected value.

The indicator LED will show which mode your board is in.

* Hue (red) - The colour of the LEDs
* Spread (green) - Deviation from  hue
* Brightness (blue) - ... the brightness :D
* Speed (yellow) - Note: lowers brightness to avoid excessive flicker when adjusting.
"""

# Set how many LEDs you have
NUM_LEDS = 26

MAX_VALUE = 100

# Pick *one* LED type by uncommenting the relevant line below:

# APA102 / DotStar™ LEDs
# led_strip = plasma.APA102(NUM_LEDS)

# WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0)


i2c = machine.I2C()
wheel = BreakoutEncoderWheel(i2c)

try:
    # RGBLED is equivalent to RGBLED("LED_R", "LED_G", "LED_B")
    led = RGBLED()
    led.set_rgb(255, 0, 0)
except ValueError:
    # Plasma Stick does not have an RGB LED so fail gracefully!
    led = None


led_strip.start()

modes = ["Hue", "Spread", "Brightness", "Speed"]
colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
values = [40, 50, 50, 50]
mode = 0
wheel_pressed = False

if led:
    led.set_rgb(*colours[mode])

while True:
    hue, spread, brightness, speed = values
    hue /= 360
    spread /= 100
    brightness /= 100
    speed /= 100

    t = time.ticks_ms() / 100 / (2 * math.pi) * speed

    if wheel.pressed(CENTRE) and not wheel_pressed:
        mode = (mode + 1) % len(modes)
        if led:
            led.set_rgb(*colours[mode])
        print(f"{modes[mode]:10}: {values[mode]:3d} / {360 if mode == 0 else 100}")

    wheel_pressed = wheel.pressed(CENTRE)

    if wheel.delta() != 0:
        if mode == 0:
            values[mode] = (values[mode] + wheel.count()) % 360
        else:
            values[mode] = min(MAX_VALUE, max(0, values[mode] + wheel.count()))
        print(f"{modes[mode]:10}: {values[mode]:3d} / {360 if mode == 0 else 100}")
        wheel.zero()

    hue_phase = 1000 * speed

    for i in range(NUM_LEDS):
        position = i / NUM_LEDS
        br = 0.5 + math.sin(t + (position * 2 * math.pi))
        br = min(1.0, max(0, br))
        br *= brightness
        hue_offset = math.sin(t + hue_phase + (position * 2 * math.pi)) / 20
        hue_offset += spread * (i / NUM_LEDS)
        hue_offset += hue
        hue_offset %= 1.0

        led_strip.set_hsv(i, hue_offset, 1.0, 0.1 if mode == 3 else br)

    # Approximately 120fps
    time.sleep(1.0 / 120)
