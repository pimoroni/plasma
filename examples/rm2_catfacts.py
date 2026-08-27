import time

import requests
from ezwifi import connect

import plasma

"""
Fetch a cat fact over an RM2 wireless module plugged into the SP/CE socket.

Plasma 2350 W has its wireless module on board and connects with a plain
connect(). A Plasma 2350 with an RM2 breakout wired to SP/CE needs
spce=True, which points the driver at those pins instead.

Add your wireless details to secrets.py before running this.
"""

URL = "http://catfact.ninja/fact"
UPDATE_INTERVAL = 60  # refresh interval in secs. Be nice to free APIs!

# Set how many LEDs you have
NUM_LEDS = 50

# Set the brightness
BRIGHTNESS = 0.5


def fill(r, g, b):
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, int(r * BRIGHTNESS), int(g * BRIGHTNESS), int(b * BRIGHTNESS))


# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_RGB)

# start updating the LED strip
led_strip.start()

# amber while we bring the wireless up
fill(255, 140, 0)

# drop spce=True on a Plasma 2350 W, where the module is already on its own pins
if connect(spce=True):
    fill(0, 255, 0)
else:
    print("Wifi connection failed!")
    fill(255, 0, 0)
    raise SystemExit

while True:
    print(f"Requesting URL: {URL}")
    response = requests.get(URL)
    fact = response.json()["fact"]
    response.close()

    print("Cat fact!")
    print(fact)

    time.sleep(UPDATE_INTERVAL)
