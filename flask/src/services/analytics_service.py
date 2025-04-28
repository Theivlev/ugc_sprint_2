import datetime
import json
import uuid

from src.core.config import nginx
from src.db.kafka import kafka_producer
from src.utils.decorators import check_auth


class Analytics:
    @check_auth(f"{nginx.dsn}/auth/v1/auth_history/all")
    def load_auth_history(data):
        """Получение данных о количестве токенов для аналитики."""
        message = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "event_id": str(uuid.uuid4()),
            "event_type": "auth_history",
            "tokens_count": len(data),
            "source_url": f"{nginx.dsn}/auth/v1/auth_history/all",
        }
        print(message)
        kafka_producer.setup()
        kafka_producer.send(
            topic="auth_history", value=json.dumps(message).encode("utf-8"), key=message["event_id"].encode("utf-8")
        )
        kafka_producer.close()
        return {"message": "Load to Kafka is success"}

    @check_auth(f"{nginx.dsn}/api/v1/films/")
    def load_lead_rating(data):
        """Получение лидера по рейтингу среди фильмов для аналитики."""
        lead_film = data[0]
        message = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "event_id": str(uuid.uuid4()),
            "event_type": "lead_film",
            "film_id": lead_film.get("id"),
            "title": lead_film.get("title"),
            "imdb_rating": lead_film.get("imdb_rating"),
            "source_url": f"{nginx.dsn}/api/v1/films/",
        }
        print(message)
        kafka_producer.setup()
        kafka_producer.send(
            topic="lead_film", value=json.dumps(message).encode("utf-8"), key=message["event_id"].encode("utf-8")
        )
        kafka_producer.close()
        return {"message": "Load to Kafka is success"}
