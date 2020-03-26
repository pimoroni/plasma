import pathlib
import yaml


class PlasmaMatrix():
    def __init__(self, config_file=None):
        self._devices = []

        if type(config_file) is str:
            config_file = pathlib.Path(config_file)
        
        if not config_file.is_file():
            raise ValueError(f"Could not find {config_file}")

        self._config = yaml.safe_load(open(config_file, "r"))

        for required in ("pixels", "devices"):
            if required not in self._config:
                raise ValueError(f"Config missing required setting: '{required}'")

        self._pixel_count = int(self._config["pixels"])

        self._pixels = [[0, 0, 0, 3]] * self._pixel_count

        for output_type, output_options in self._config["devices"].items():
            print(output_type, output_options)

            pixels = output_options.get("pixels", self._pixel_count)
            pixels_per_light = output_options.get("pixels_per_light", 1)
            offset = output_options.get("offset", 0)

            del output_options["pixels"]
            del output_options["offset"]

            output_device = self.get_output_device(output_type)

            self._devices.append({
                'offset': offset,
                'device': output_device(pixels // pixels_per_light, **output_options)
            })

    def get_pixel_count(self):
        """Get the count of pixels."""
        return self._pixel_count

    def get_device_count(self):
        """Get the count of output devices."""
        return len(self._devices)

    def get_output_device(self, output_type):
        """Get output class by name."""
        if output_type in ["GPIO", "APA102"]:
            from .gpio import PlasmaGPIO
            return PlasmaGPIO
        if output_type in ["USB", "SERIAL"]:
            from .usb import PlasmaSerial
            return PlasmaSerial
        if output_type == "WS281X":
            from .ws281x import PlasmaWS281X
            return PlasmaWS281X

    def show(self):
        """Display lights across devices.

        Sets each device in turn, picking the pixels
        from the buffer starting from the specified offset.

        """
        for d in self._devices:
            device = d.get('device')
            offset = d.get('offset')
            for x in range(device.get_pixel_count()):
                r, g, b, br = self._pixels[offset + x]
                device.set_pixel(x, r, g, b)
            device.show()
