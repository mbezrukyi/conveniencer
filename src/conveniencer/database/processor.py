from typing import List, Type

from motor.motor_asyncio import AsyncIOMotorCollection

from .entities import Entity
from .errors import NoDocumentError


class CollectionProcessor:
    def __init__(
        self,
        user_id: str,
        collection: AsyncIOMotorCollection,
        type_: Type[Entity],
    ):
        self._user_id = user_id
        self._collection = collection
        self._type = type_

    async def add(self, entity: Entity) -> None:
        await self._collection.insert_one(
            {"user_id": self._user_id, **entity.to_dict()}
        )

    async def replace(self, entity: Entity) -> None:
        await self._collection.update_one(
            {"user_id": self._user_id, **entity.by},
            {"$set": entity.to_dict()},
        )

    async def remove(self, entity: Entity) -> None:
        result = await self._collection.delete_one(
            {"user_id": self._user_id, **entity.by}
        )

        if result.modified_count == 0:
            raise NoDocumentError("No document was found to delete.")

    async def to_list(self) -> List[Entity]:
        return [
            self._type(**document)
            for document in await self._collection.find(
                {"user_id": self._user_id},
                projection={
                    "_id": False,
                    "user_id": False,
                },
            ).to_list(length=None)
        ]
