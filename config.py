import toml


class _Config:
    def __init__(self):
        self.xLeft = 0
        self.xRight = 0
        self.yTop = 0
        self.yBottom = 0

    def load_configuration(self, filename, **kwargs):
        config_file = toml.load(filename)
        self.xLeft = config_file['screenMargins']['xLeft']
        self.xRight = config_file['screenMargins']['xRight']
        self.yTop = config_file['screenMargins']['yTop']
        self.yBottom = config_file['screenMargins']['yBottom']
        [setattr(self, k, v) for (k, v) in kwargs.items()]
        [setattr(self, k, v) for (k, v) in config_file.items()]

    def __repr__(self):
        return str(self.__dict__)


config = _Config()


def set_config(filename: str):
    config.load_configuration(filename)
