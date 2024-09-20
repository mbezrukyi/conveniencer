from typing import List, Type

from motor.motor_asyncio import AsyncIOMotorCollection

from .documents import Document
from .errors import NoDocumentError


class CollectionProcessor:
    def __init__(
        self,
        collection: AsyncIOMotorCollection,
        type_: Type[Document],
    ):
        self._collection = collection
        self._type = type_

    async def add(self, entity: Document) -> None:
        await self._collection.insert_one(entity.to_dict())

    async def replace(self, entity: Document) -> None:
        await self._collection.update_one(
            entity.by(),
            {"$set": entity.to_dict()},
        )

    async def remove(self, entity: Document) -> None:
        result = await self._collection.delete_one(entity.by())

        if result.deleted_count == 0:
            raise NoDocumentError("No document was found to delete.")

    async def to_list(self, user_id: str) -> List[Document]:
        return [
            self._type(**document)
            for document in await self._collection.find(
                {"user_id": user_id},
                projection={"_id": False},
            ).to_list(length=None)
        ]
