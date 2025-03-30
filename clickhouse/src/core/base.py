import abc
from typing import AsyncGenerator, List
from aiokafka import ConsumerRecord
from contextlib import asynccontextmanager


class BaseMessageReader(abc.ABC):
    """Абстрактный базовый класс для чтения сообщений из брокеров."""

    @abc.abstractmethod
    async def read(self, batch_size: int = 10) -> AsyncGenerator[List[bytes], None]:
        """Асинхронное чтение сообщений."""
        pass

    @abc.abstractmethod
    async def commit(self):
        """Подтверждение обработанных сообщений."""
        pass

    @abc.abstractmethod
    @asynccontextmanager
    async def connect(self):
        """Управление соединением с брокером."""
        pass


class BaseWriter(abc.ABC):
    """Абстрактный базовый класс для записи данных."""

    @abc.abstractmethod
    async def write(self, rows: List[dict]):
        """
        Запись данных.
        """
        pass

    @abc.abstractmethod
    @asynccontextmanager
    async def connect(self):
        """Управление соединением с бд."""
        pass


class BaseMessageTranformer(abc.ABC):
    """Абстрактный базовый класс для трансформации сообщений."""

    @abc.abstractmethod
    async def transoform(self, messages: List[ConsumerRecord]) -> AsyncGenerator[tuple, None]:
        """Асинхронный метод для трансформации сообщений."""
        pass
