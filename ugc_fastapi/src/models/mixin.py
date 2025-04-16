from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator
from src.utils.json_loads_or_dumps import orjson, orjson_dumps
from src.models.dto import AbstractDTO
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        """
        Определяет, как Pydantic должен работать с PyObjectId.
        """
        return core_schema.no_info_after_validator_function(
            cls.validate,
            handler(str),
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        """
        Валидирует значение как ObjectId.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Некорректный ObjectId")
        return ObjectId(v)


class OrjsonMixin(AbstractDTO):
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