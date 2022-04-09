import configparser


class Config:

    def __init__(self, config_file: str = "config.ini") -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    @property
    def token(self) -> str:
        return self.config.get("DEFAULT", "token")
