"""Colour diagnostic: lights up all LEDs with one colour at a time.
Press Enter in the REPL to advance to the next colour.
Report back what you actually see for each one!
"""
import time
import plasma

NUM_LEDS = 50
TEST_LEDS = 10  # only light first 10 to save power
led_strip = plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_BGR)
led_strip.start()

colors = [
    ("RED",     255,   0,   0),
    ("GREEN",     0, 255,   0),
    ("BLUE",      0,   0, 255),
    ("YELLOW",  255, 255,   0),
    ("CYAN",      0, 255, 255),
    ("MAGENTA", 255,   0, 255),
    ("WHITE",   255, 255, 255),
]

for name, r, g, b in colors:
    for i in range(TEST_LEDS):
        led_strip.set_rgb(i, r, g, b)
    print(f"Sending: {name} (R={r}, G={g}, B={b})")
    print("  -> What colour do you see? Press Enter for next...")
    input()
    # Turn off before next colour
    for i in range(TEST_LEDS):
        led_strip.set_rgb(i, 0, 0, 0)

print("Done!")
