from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.formatting import as_section

from .utils import build_text_commands

router = Router(name=__name__)


@router.message(Command("commands"))
async def command_commands_handler(message: Message) -> None:
    content = as_section(
        "List of commands:",
        *build_text_commands(),
    )

    await message.answer(**content.as_kwargs())
