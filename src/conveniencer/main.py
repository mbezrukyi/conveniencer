import asyncio
from aiogram import Bot, Dispatcher
from motor.motor_asyncio import AsyncIOMotorClient

from conveniencer import handlers
from conveniencer.config import load_config


async def main() -> None:
    config = load_config(".bot")

    mongo = AsyncIOMotorClient(
        host=config.mongo.host,
        port=config.mongo.port,
        username=config.mongo.username,
        password=config.mongo.password,
    )
    db = mongo.conviniencer

    bot = Bot(token=config.bot.token)

    dp = Dispatcher(db=db)
    dp.include_routers(
        handlers.router,
    )

    return await dp.start_polling(bot)


def cli() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    cli()
