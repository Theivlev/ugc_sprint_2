from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator
from utils.json_loads_or_dumps import orjson, orjson_dumps


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        """Настройка JSON-схемы для отображения ObjectId как строки."""
        schema = handler(core_schema)
        schema.update(type="string")
        return schema

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        """Валидация значения как ObjectId."""
        if not ObjectId.is_valid(v):
            raise ValueError("Некорректный ObjectId")
        return ObjectId(v)


class OrjsonMixin(BaseModel):
    """Базовый класс для ускоренной обработки JSON."""

    model_config = ConfigDict(
        json_loads=orjson.loads,
        json_dumps=lambda v, *, default: orjson_dumps(v, default=default).decode(),
    )


class ObjectIdMixin(OrjsonMixin):
    """Базовый класс для работы с MongoDB `_id`."""

    id: Annotated[PyObjectId, Field(alias="_id", default=None)]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_loads=orjson.loads,
        json_dumps=lambda v, *, default: orjson_dumps(v, default=default).decode(),
    )

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> ObjectId:
        """Валидация поля id как ObjectId."""
        return PyObjectId.validate(v)
