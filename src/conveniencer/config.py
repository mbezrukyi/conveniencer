from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class Bot:
    token: str


@dataclass
class Config:
    bot: Bot


def load_config(path: str) -> Config:
    config = ConfigParser()
    config.read(path)

    bot = config["bot"]

    return Config(
        bot=Bot(
            token=bot.get("token"),
        )
    )
