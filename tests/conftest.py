import pytest_asyncio
from cock import Config
from testcontainers.postgres import PostgresContainer
from yarl import URL

from alco_map.database.models import Base
from alco_map.database import database_from_config


def pytest_addoption(parser):
    parser.addoption("--local-dsn", action="store", default=False)


@pytest_asyncio.fixture(scope="session")
def local_dsn(request):
    return request.config.getoption("--local-dsn")


@pytest_asyncio.fixture(scope="session")
def db_dsn(local_dsn):
    if local_dsn:
        yield local_dsn
    else:
        with PostgresContainer("postgis/postgis:14-3.2-alpine", dbname="alco-map") as pg:
            connection_url = pg.get_connection_url()
            yield URL(connection_url).with_scheme("postgresql+asyncpg")


@pytest_asyncio.fixture(scope="session")
def config(db_dsn):
    u = URL(db_dsn)
    cfg = Config({
        "db_host": u.host,
        "db_port": u.port,
        "db_user": u.user,
        "db_password": u.password,
        "db_database": u.path.lstrip("/")
    })
    return cfg


@pytest_asyncio.fixture
async def db(config):
    db = database_from_config(config)
    async with db:
        yield db
        async with db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
