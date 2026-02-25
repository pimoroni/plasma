import time

from pimoroni import RGBLED, Analog, Button

import plasma

"""
- Press "B" to speed up the LED cycling effect.
- Press "A" to slow it down again.
- Press "Boot" to reset the speed back to default.
"""

# Set how many LEDs you have
NUM_LEDS = 30

# The speed that the LEDs will start cycling at
DEFAULT_SPEED = 10

# How many times the LEDs will be updated per second
UPDATES = 60

# Magic values for Plasma 2040 current sense
# 3A * 0.015Ω = 0.045V
# 0.045V * 50 (gain) = 2.25V maximum
ADC_GAIN = 50
SHUNT_RESISTOR = 0.015

# Pick *one* LED type by uncommenting the relevant line below:

# APA102 / DotStar™ LEDs
# led_strip = plasma.APA102(NUM_LEDS)

# WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS)

user_sw = Button("USER_SW", repeat_time=0)
button_a = Button("BUTTON_A", repeat_time=0)
try:
    # Button B is only available on Plasma 2040
    button_b = Button("BUTTON_B", repeat_time=0)
except ValueError:
    button_b = None
led = RGBLED("LED_R", "LED_G", "LED_B")

try:
    # Sense is only available on Plasma 2040
    sense = Analog("CURRENT_SENSE", ADC_GAIN, SHUNT_RESISTOR)
except ValueError:
    sense = None

# Start updating the LED strip
led_strip.start()

speed = DEFAULT_SPEED
offset = 0.0

count = 0
# Make rainbows
while True:
    sw = user_sw.read()
    a = button_a.read()
    b = button_b and button_b.read()

    if sw:
        speed = DEFAULT_SPEED
    else:
        if a:
            speed -= 1
        if b:
            speed += 1

    speed = min(255, max(1, speed))

    offset += float(speed) / 2000.0

    for i in range(NUM_LEDS):
        hue = float(i) / NUM_LEDS
        led_strip.set_hsv(i, hue + offset, 1.0, 1.0)

    led.set_rgb(speed, 0, 255 - speed)

    count += 1
    if sense and count >= UPDATES:
        # Display the current value once every second
        print("Current =", sense.read_current(), "A")
        count = 0

    time.sleep(1.0 / UPDATES)
