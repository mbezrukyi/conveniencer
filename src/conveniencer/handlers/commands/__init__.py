from aiogram import Router

from . import categories, commands, start

router = Router(name="commands")

router.include_routers(
    categories.router,
    commands.router,
    start.router,
)
