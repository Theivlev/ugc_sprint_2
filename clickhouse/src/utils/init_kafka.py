import logging
from aiokafka.errors import KafkaError, TopicAlreadyExistsError
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_topic(admin_client: AIOKafkaAdminClient):
    try:
        existing_topics = await admin_client.list_topics()
        if settings.topic in existing_topics:
            logger.info(f"Топик '{settings.topic}' уже существует, пропускаем создание.")
            return

        topic = NewTopic(
            name=settings.topic,
            num_partitions=settings.partitions,
            replication_factor=settings.replication_factor,
            topic_configs={
                "min.insync.replicas": settings.replicas,
                "retention.ms": settings.time_to_retain_data
            }
        )
        logger.info(f"Создаём топик '{settings.topic}'...")
        await admin_client.create_topics([topic])
        logger.info(f"Топик '{settings.topic}' успешно создан!")
        logger.info(f'Факторе репликации: {settings.replication_factor}')
        logger.info(f'Кол-во партиций: {settings.partitions}')
    except TopicAlreadyExistsError:
        logger.info(f"Топик '{settings.topic}' уже существует, создание не требуется.")
    except KafkaError as e:
        logger.error(f"Ошибка при создании топика '{settings.topic}': {e}")
        raise


async def init_kafka():
    admin_client = AIOKafkaAdminClient(
        bootstrap_servers=settings.kafka_brokers[0]
    )
    try:
        logger.info(f"Подключаемся к Kafka брокерам: {settings.kafka_brokers[0]}")
        await admin_client.start()
        await create_topic(admin_client)
    except KafkaError as e:
        logger.error(f"Не удалось инициализировать Kafka: {e}")
        raise
    finally:
        await admin_client.close()
        logger.info("Admin client закрыт.")
