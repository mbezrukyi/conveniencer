from aiogram import Router

from . import categories

router = Router(name="callback_queries")

router.include_routers(
    categories.router,
)
