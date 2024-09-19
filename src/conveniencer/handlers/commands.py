from collections import namedtuple
from typing import List

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command, CommandStart
from aiogram.utils.formatting import (
    Bold,
    Text,
    as_list,
    as_section,
)

from .keyboards import build_categories_keyboard

router = Router(name=__name__)

ConveniencerCommand = namedtuple("ConveniencerCommand", ["name", "desc"])

commands_list: List[ConveniencerCommand] = [
    ConveniencerCommand(name="start", desc="Start bot"),
    ConveniencerCommand(name="categories", desc="List categories"),
    ConveniencerCommand(name="help", desc="List commands"),
]


def build_text_commands() -> List[Text]:
    return [
        Text(Bold(i), ". /", command.name, " - ", command.desc, "\n")
        for i, command in enumerate(commands_list, start=1)
    ]


@router.message(CommandStart())
async def handle_start_command(message: Message) -> None:
    content = as_list(
        Text("Hi, ", Bold(message.from_user.full_name), "!\n"),
        as_section(
            "Commands list:",
            *build_text_commands(),
        ),
    )

    await message.answer(**content.as_kwargs())


@router.message(Command("categories"))
async def handle_categories_command(message: Message) -> None:
    await message.answer(
        text="Categories list:",
        reply_markup=build_categories_keyboard(),
    )


@router.message(Command("help"))
async def handle_help_command(message: Message) -> None:
    content = as_section(
        "Commands list:",
        *build_text_commands(),
    )

    await message.answer(**content.as_kwargs())
