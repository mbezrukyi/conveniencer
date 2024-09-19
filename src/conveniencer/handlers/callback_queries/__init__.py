from aiogram import Router
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from . import archive, back, book, link, photo

router = Router(name="callback_queries")
router.callback_query.middleware(CallbackAnswerMiddleware(cache_time=3))

router.include_routers(
    archive.router,
    back.router,
    book.router,
    link.router,
    photo.router,
)
