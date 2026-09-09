require("bundle-networking")
require("urllib.urequest")
require("umqtt.simple")

# Bluetooth
require("aioble")

include("../manifest-common.py")

freeze("../../modules/wireless/")

# The SP/CE screen library, from the spidisplay clone beside this one, frozen so one
# uf2 carries it
freeze("$(PORT_DIR)/../../../spidisplay/src")
