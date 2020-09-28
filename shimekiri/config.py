import os
import platform
import shutil
from shimekiri import Logger
from shimekiri import fileFn
from shimekiri import directories


class Config:
    @classmethod
    def load(cls):
        return fileFn.load_json(cls.get_config_file())

    @classmethod
    def update(cls, new_config_dict):
        current_config: dict = cls.load()
        current_config.update(new_config_dict)
        fileFn.write_json(cls.get_config_file(), current_config)

    @classmethod
    def get(cls, key, default=None):
        current_config: dict = cls.load()
        if key not in current_config.keys():
            current_config[key] = default
            cls.update(current_config)
        return current_config.get(key)

    @classmethod
    def set(cls, key, value):
        cls.update({key: value})

    @classmethod
    def reset(cls):
        config_dir = Config.get_config_dir()
        config_file = os.path.join(config_dir, "shimekiri_config.json")
        shutil.copy2(directories.DEFAULT_CONFIG, config_file)
        Logger.info("Shimekiri config reset to default")

    @staticmethod
    def get_config_dir():
        if platform.system() == "Darwin":
            config_dir = os.path.join(os.path.expanduser("~/Library/Preferences"), "shimekiri")
        elif platform.system() == "Windows":
            config_dir = os.path.join(os.getenv("LOCALAPPDATA"), "shimekiri")
        fileFn.create_missing_dir(config_dir)

        return config_dir

    @ staticmethod
    def get_config_file():
        config_dir = Config.get_config_dir()
        config_file = os.path.join(config_dir, "shimekiri_config.json")
        if not os.path.isfile(config_file):
            shutil.copy2(directories.DEFAULT_CONFIG, config_file)
            Logger.debug("Default config copied to: {0}".format(config_file))

        return config_file


if __name__ == "__main__":
    pass
