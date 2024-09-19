from aiogram import Router

from . import archive, book, link, photo

router = Router(name="callback_queries")

router.include_routers(
    archive.router,
    book.router,
    link.router,
    photo.router,
)
