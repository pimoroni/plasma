import pathlib
import yaml


class PlasmaMatrix():
    def __init__(self, config_file=None):
        if type(config_file) is str:
            config_file = pathlib.Path(config_file)
        
        if not config_file.is_file():
            raise ValueError(f"Could not find {config_file}")

        self._config = yaml.safe_load(open(config_file, "r"))
