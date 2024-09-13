from typing import List, Type

from motor.motor_asyncio import AsyncIOMotorCollection

from .entities import Entity


class CollectionProcessor:
    def __init__(self, collection: AsyncIOMotorCollection):
        self._collection = collection

    async def add(self, entity: Entity) -> None:
        await self._collection.insert_one(entity.data)

    async def remove(self, entity: Entity) -> None:
        await self._collection.delete_one(entity.remove_by)

    async def update(self, entity: Entity) -> None:
        await self._collection.update_one(
            entity.update_by,
            {"$set": entity.update_data},
        )

    async def to_list(self, type_: Type[Entity]) -> List[Entity]:
        return [
            type_(**document)
            for document in await self._collection.find(
                projection={"_id": False}
            ).to_list(length=None)
        ]
