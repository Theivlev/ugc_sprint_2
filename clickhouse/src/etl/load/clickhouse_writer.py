from aiochclient import ChClient
from aiohttp import ClientSession

from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import List
from core.config import settings
from core.base import BaseWriter
from models.message import MessageDTO
from .query import QueryBuilder


@dataclass
class ClickHouseWriter(BaseWriter):
    """Реализация записи данных в ClickHouse."""
    session: ClientSession = None
    client: ChClient = None
    query_builder: QueryBuilder = QueryBuilder()

    @asynccontextmanager
    async def connect(self):
        """
        Асинхронный контекстный менеджер для управления соединением с ClickHouse.
        """
        try:
            self.session = ClientSession()
            self.client = ChClient(self.session, settings.clickhouse_nodes[0])
            yield self
        except Exception as e:

            raise e
        finally:
            if self.session:
                await self.session.close()

    async def write(self, rows: List[MessageDTO]):
        """
        Запись данных в ClickHouse.
        """
        try:
            query = self.query_builder.build_insert_query(
                table_name='data_analytics.event_table',
                model_class=MessageDTO
            )
            await self.client.execute(query, *rows)
        except Exception as e:
            raise e