from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import (
    as_list,
    as_section,
    Bold,
    Text,
)

from .utils import build_text_commands

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    content = as_list(
        Text("Hi, ", Bold(message.from_user.full_name), "!\n"),
        as_section(
            "Here's the list of available commands:",
            *build_text_commands(),
        ),
    )

    await message.answer(**content.as_kwargs())
