from aiokafka import AIOKafkaConsumer
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List

from core.config import settings
from core.base import BaseMessageReader


class KafkaReader(BaseMessageReader):
    """Реализация чтения сообщений из Kafka."""

    def __init__(self):
        self.consumer = None

    @asynccontextmanager
    async def connect(self):
        """
        Асинхронный контекстный менеджер для управления соединением с Kafka.
        """
        try:
            self.consumer = AIOKafkaConsumer(
                settings.topic,
                bootstrap_servers=settings.kafka_brokers,
                group_id=settings.group_id,
                auto_offset_reset="earliest",
                enable_auto_commit=False,
            )
            await self.consumer.start()
            yield self
        except Exception as e:
            raise e
        finally:
            if self.consumer:
                await self.consumer.stop()

    async def read(self, batch_size: int = 10) -> AsyncGenerator[List[bytes], None]:
        """
        Асинхронное чтение сообщений пакетами заданного размера.
        """
        messages = []

        try:
            async for message in self.consumer:
                messages.append(message.value)

                if len(messages) >= batch_size:
                    yield messages
                    messages.clear()
        except Exception as e:
            raise e

    async def commit(self):
        """
        Подтверждение обработанных сообщений.
        """
        try:
            if self.consumer:
                await self.consumer.commit()
        except Exception as e:
            raise e
