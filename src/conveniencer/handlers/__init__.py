from aiogram import Router

from . import callback_queries, commands

router = Router(name="handlers")

router.include_routers(
    callback_queries.router,
    commands.router,
)
