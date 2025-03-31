import asyncio
import logging

import aio_pika
import backoff
from aio_pika.exceptions import AMQPConnectionError, ChannelClosed, ConnectionClosed
from core.config import rabbit_settings

logger = logging.getLogger(__name__)


async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    """Обработка сообщения из очереди."""

    async with message.process():
        print(message.body)
        await asyncio.sleep(1)


@backoff.on_exception(backoff.expo, (AMQPConnectionError, ConnectionClosed, ChannelClosed))
async def main() -> None:
    """Основная функция с подключением к RabbitMQ и обработкой сообщений."""
    logger.info("Подключение к RabbitMQ")
    connection = await aio_pika.connect_robust(
        login=rabbit_settings.user,
        password=rabbit_settings.password,
        host=rabbit_settings.host,
        port=rabbit_settings.port,
        virtual_host="/",
    )
    logger.info("Подключение к каналу RabbitMQ")
    channel = await connection.channel()
    queue = await channel.declare_queue("mail", durable=True)

    logger.info("Начало приема сообщений")
    await queue.consume(process_message)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    logger.info("Старт сервиса")
    asyncio.run(main())
