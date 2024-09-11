from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text

from ..keyboards import build_categories_keyboard

router = Router(name=__name__)


@router.message(Command("categories"))
async def command_categories_handler(message: Message) -> None:
    content = Text("Available categories:")

    await message.answer(
        **content.as_kwargs(),
        reply_markup=build_categories_keyboard(),
    )
