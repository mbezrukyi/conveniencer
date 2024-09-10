from aiogram import Router

from . import commands, start

router = Router(name="commands")

router.include_routers(
    commands.router,
    start.router,
)
