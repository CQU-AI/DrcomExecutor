from pathlib import Path

import yaml


class Config:
    path = Path(__file__).parent / "config.yaml"

    def __init__(self):
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
        (Path(__file__).parent / "config.yaml").write_text(
            (Path(__file__).parent / "config_default.yaml").read_text()
        )


config = Config()
