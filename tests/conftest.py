import pytest
from testcontainers.postgres import PostgresContainer

from alco_map.database.methods import StoreManage
from alco_map.database.models import Base


def pytest_addoption(parser):
    parser.addoption("--local-dsn", action="store", default=False)


@pytest.fixture
async def store(request):
    connection_url = request.config.getoption("--local-dsn")
    if not connection_url:
        postgres_container = PostgresContainer("postgis/postgis:14-3.2-alpine", dbname="alco-map")
        postgres = postgres_container.start()
        connection_url = postgres.get_connection_url().replace("psycopg2", "asyncpg")
    store = StoreManage()
    store.connection_url = connection_url
    async with store.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return store
