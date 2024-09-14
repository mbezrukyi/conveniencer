import re

from aiogram.filters import Filter
from aiogram.types import Message


class LinkFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return bool(
            re.match(
                r"^\w+:\s*?(http|https):\/\/[a-zA-Z0-9]+?\.[a-zA-Z]\S*?$",
                message.text,
            )
        )
