#!/usr/bin/env bash
set -e

echo "Waiting for PostgreSQL to be ready..."
python << END
import time
import asyncpg
import asyncio
import os

dsn = os.environ.get("POSTGRES_DSN")
if dsn:
    async def wait_for_db():
        while True:
            try:
                conn = await asyncpg.connect(dsn)
                await conn.close()
                break
            except Exception as e:
                print(f"PostgreSQL is not ready yet: {e}. Sleeping...")
                time.sleep(2)

    asyncio.run(wait_for_db())
    print("PostgreSQL is up!")
END

# echo "Running Alembic migrations..."
# alembic upgrade head

# Запуск переданного процесса (с переменными окружения)
echo "Starting main process: $@"
exec "$@"
