require("bundle-networking")
require("urllib.urequest")
require("umqtt.simple")

# Bluetooth
require("aioble")

include("../manifest-common.py")

freeze("../../modules/wireless/")
