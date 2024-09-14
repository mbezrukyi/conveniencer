from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class Bot:
    token: str


@dataclass
class Mongo:
    host: str
    port: int
    username: str
    password: str


@dataclass
class Config:
    bot: Bot
    mongo: Mongo


def load_config(path: str) -> Config:
    config = ConfigParser()
    config.read(path)

    bot = config["bot"]
    mongo = config["mongo"]

    return Config(
        bot=Bot(token=bot.get("token")),
        mongo=Mongo(
            host=mongo.get("host"),
            port=mongo.getint("port"),
            username=mongo.get("username"),
            password=mongo.get("password"),
        ),
    )
