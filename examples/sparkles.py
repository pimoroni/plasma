import math
import time

import plasma

NUM_LEDS = 26
EFFECT_SPEED = 2       # Does what it says on the tin! (lower is slower but you might see quantization/stepping)
EFFECT_SHARPNESS = 10  # Numbers between 1 and 1000 are practical, give them a try!
EFFECT_FPS = 60        # You'll probably never need to change this

led_strip = plasma.WS2812(NUM_LEDS)
led_strip.start()

period = math.pi * EFFECT_SPEED

try:
    while True:
        t = time.ticks_ms() / 1000 * period
        t *= 0.5

        for i in range(NUM_LEDS):
            led_offset = i / NUM_LEDS
            led_offset *= math.pi
            led_offset *= 3
            led_offset += t

            # A simple sine with a 2x period, shifted to 0 to 254
            # This provides a brightness cycling effect phase-locked to the LEDs
            br = (math.sin(t / 2 + led_offset) + 1) * 127

            # Calculate slightly out of phase sine waves for the red, green and blue channels
            r = (math.sin(led_offset + (period * 0.85)) + 1) / 2
            g = (math.sin(led_offset + (period * 0.90)) + 1) / 2
            b = (math.sin(led_offset + (period * 0.95)) + 1) / 2

            # Convert the slow procession of the sine wave into a brief pulse
            # by raising it by a power we've called EFFECT_SHARPNESS
            # https://www.wolframalpha.com/input?i=plot+pow%28%28sin%28x%29+%2B+1%29+%2F+2.0%2C+10%29%2C+%28sin%28x%29+%2B+1%29+%2F+2.0
            r = min(1, max(0, math.pow(r, EFFECT_SHARPNESS)))
            g = min(1, max(0, math.pow(g, EFFECT_SHARPNESS)))
            b = min(1, max(0, math.pow(b, EFFECT_SHARPNESS)))

            # Tune the output colours and apply brightness
            # This is a nice greeny teal
            r = 0
            g = int(g * br)
            b = int(g * 0.6)

            led_strip.set_rgb(i, g, r, b)

        time.sleep(1.0 / EFFECT_FPS)
finally:
    led_strip.clear()
    led_strip.stop()
