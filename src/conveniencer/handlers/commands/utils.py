from collections import namedtuple
from typing import List

from aiogram.utils.formatting import Bold, Code, Text

Command = namedtuple("Command", ["name", "desc"])

commands_list: List[Command] = [
    Command(name="start", desc="Start bot"),
    Command(name="categories", desc="List categories"),
    Command(name="help", desc="List commands"),
]


def create_command_text(command: Command) -> Text:
    return Text(Code(f"/{command.name}"), f" - {command.desc}")


def build_text_commands() -> List[Text]:
    return [
        Text(Bold(f"{i}."), " ", create_command_text(command), "\n")
        for i, command in enumerate(commands_list, start=1)
    ]
