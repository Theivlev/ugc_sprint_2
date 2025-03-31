from aiokafka import AIOKafkaConsumer
from typing import AsyncGenerator, List
from dataclasses import dataclass
from core.config import settings
from core.base import BaseMessageReader


@dataclass
class KafkaReader(BaseMessageReader):
    consumer: AIOKafkaConsumer = None

    async def __aenter__(self):
        self.consumer = AIOKafkaConsumer(
            settings.topic,
            bootstrap_servers=settings.kafka_brokers,
            group_id=settings.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
        )
        await self.consumer.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.consumer:
            await self.consumer.stop()

    async def read(self, batch_size: int = 10) -> AsyncGenerator[List[bytes], None]:
        messages = []

        try:
            async for message in self.consumer:
                messages.append(message.value)

                if len(messages) >= batch_size:
                    yield messages
                    messages.clear()
        finally:
            if messages:
                yield messages

    async def commit(self):
        if self.consumer:
            await self.consumer.commit()
