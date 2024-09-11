from aiogram.filters import Filter
from aiogram.types import Message


class DocumentTypeFilter(Filter):
    def __init__(self, extension: str):
        self._extension = extension

    async def __call__(self, message: Message) -> bool:
        return message.document.file_name.endswith(self._extension)
