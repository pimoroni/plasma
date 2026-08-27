import network
from ezwifi import connect
from phew import server
from phew.template import render_template
from pimoroni import RGBLED

import plasma

"""
Serve a web page with a colour picker on it, and set your LED strip to
whatever colour is picked.

Needs phew, which is not built into the firmware. In Thonny pick
Tools > Manage Packages and search for "micropython-phew".

Add your wireless details to secrets.py before running this.
"""

# Set how many LEDs you have
NUM_LEDS = 50

# The colour the picker starts on
last_hex = "#ffffff"

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_RGB)

# start updating the LED strip
led_strip.start()

try:
    # RGBLED is equivalent to RGBLED("LED_R", "LED_G", "LED_B")
    led = RGBLED()
except ValueError:
    # Plasma Stick does not have an RGB LED so fail gracefully!
    led = None


# converts a hex colour code into RGB
def hex_to_rgb(hex):
    h = hex.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def set_everything(r, g, b):
    if led:
        led.set_rgb(r, g, b)
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, r, g, b)


# there's only one page, so serve it for both the GET and the POST
@server.route("/", methods=["GET", "POST"])
def index(request):
    global last_hex

    if request.method == "POST":
        last_hex = request.form["rgbled"]
        set_everything(*hex_to_rgb(last_hex))

    # last_hex has to be passed in, the template cannot see our globals
    return render_template("html/index.html", last_hex=last_hex)


@server.catchall()
def catchall(_request):
    return "Not found", 404


if not connect():
    raise SystemExit("Wifi connection failed!")

print(f"Point a browser at http://{network.WLAN(network.STA_IF).ipconfig('addr4')[0]}")

server.run()
