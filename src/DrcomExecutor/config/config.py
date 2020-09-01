from pathlib import Path

import yaml


class Config:
    path = Path(__file__).parent / "config.yaml"
    default_path = Path(__file__).parent / "config_default.yaml"

    def __init__(self):
        if not self.path.is_file():
            if not self.default_path.is_file():
                raise FileNotFoundError("所有配置文件都已损坏!")
            else:
                Config.reset()
        self.data = self.read_yaml(self.path)

    @staticmethod
    def read_yaml(file_path):
        data = yaml.load(file_path.read_text(), Loader=yaml.SafeLoader)
        return data

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def dump(self):
        self.path.write_text(yaml.dump(self.data, Dumper=yaml.SafeDumper))

    @classmethod
    def reset(cls):
        cls.path.write_text(cls.default_path.read_text())


config = Config()
