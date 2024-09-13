from typing import Any, Dict, List

from motor.motor_asyncio import AsyncIOMotorCollection


class CollectionProcessor:
    def __init__(self, collection: AsyncIOMotorCollection):
        self._collection = collection

    async def add(self, data: Dict[str, Any]) -> None:
        await self._collection.insert_one(data)

    async def remove(self, by: Dict[str, Any]) -> None:
        await self._collection.delete_one(by)

    async def update(self, by: Dict[str, Any], data: Dict[str, Any]) -> None:
        await self._collection.update_one(by, {"$set": data})

    async def to_list(self) -> List[Any]:
        return await self._collection.find().to_list(length=None)
