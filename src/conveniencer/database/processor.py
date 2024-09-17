from typing import List, Type

from motor.motor_asyncio import AsyncIOMotorCollection

from .entities import Entity
from .errors import NoDocumentError


class CollectionProcessor:
    def __init__(
        self,
        collection: AsyncIOMotorCollection,
        type_: Type[Entity],
    ):
        self._collection = collection
        self._type = type_

    async def add(self, entity: Entity) -> None:
        await self._collection.insert_one(entity.data)

    async def replace(self, entity: Entity) -> None:
        await self._collection.update_one(
            entity.by,
            {"$set": entity.replace},
        )

    async def remove(self, entity: Entity) -> None:
        result = await self._collection.delete_one(entity.by)

        if result.deleted_count == 0:
            raise NoDocumentError("No document was found to delete.")

    async def to_list(self) -> List[Entity]:
        return [
            self._type(**document)
            for document in await self._collection.find(
                projection={"_id": False}
            ).to_list(length=None)
        ]
