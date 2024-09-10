import asyncio
from aiogram import Bot, Dispatcher

from conveniencer.config import load_config


async def main() -> None:
    config = load_config(".bot")

    bot = Bot(token=config.bot.token)

    dp = Dispatcher()

    return await dp.start_polling(bot)


def cli() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    cli()
