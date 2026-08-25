include("$(PORT_DIR)/boards/manifest.py")

# Handy for dealing with APIs
require("datetime")

freeze("$(BOARD_DIR)", "version.py")
freeze("../modules/common/")
