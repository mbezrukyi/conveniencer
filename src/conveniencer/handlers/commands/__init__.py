from aiogram import Router

from . import categories, help, start

router = Router(name="commands")

router.include_routers(
    categories.router,
    help.router,
    start.router,
)
