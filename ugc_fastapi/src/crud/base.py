from typing import Generic, List, Optional, Type, TypeVar

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseMongoCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, collection: AsyncIOMotorCollection, model: Type[ModelType]):
        """
        Инициализация CRUD-сервиса.
        :param collection: Коллекция MongoDB.
        :param model: Pydantic-модель для валидации данных.
        """
        self.collection = collection
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        """
        Создает новый документ в коллекции.
        """
        insert_data = data.model_dump(exclude_none=True)
        result = await self.collection.insert_one(insert_data)
        created_doc = await self.collection.find_one({"_id": result.inserted_id})
        return self.model(**created_doc)

    async def get(self, id_: str) -> Optional[ModelType]:
        """
        Получает документ по ID.
        """
        doc = await self.collection.find_one({"_id": ObjectId(id_)})
        if doc:
            return self.model(**doc)
        return None

    async def find(self, filter_: dict, page_number: int = 0, page_size: int = 10) -> List[ModelType]:
        """
        Ищет документы с пагинацией.
        """
        skip = page_number * page_size
        cursor = self.collection.find(filter_).skip(skip).limit(page_size)
        docs = await cursor.to_list(length=None)
        return [self.model(**doc) for doc in docs]

    async def update(self, id_: str, data: UpdateSchemaType) -> Optional[ModelType]:
        """
        Обновляет документ по ID.
        """
        update_data = {"$set": data.model_dump(exclude_none=True)}
        await self.collection.update_one({"_id": ObjectId(id_)}, update_data)
        updated_doc = await self.collection.find_one({"_id": ObjectId(id_)})
        if updated_doc:
            return self.model(**updated_doc)
        return None

    async def delete(self, id_: str) -> bool:
        """
        Удаляет документ по ID.
        """
        result = await self.collection.delete_one({"_id": ObjectId(id_)})
        return result.deleted_count > 0
