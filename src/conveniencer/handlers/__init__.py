from aiogram import Router

from . import commands

router = Router(name="handlers")

router.include_routers(
    commands.router,
)
