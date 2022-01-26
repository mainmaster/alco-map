import pytest
from shapely import wkb
from sqlalchemy.future import select
from testcontainers.postgres import PostgresContainer

from alco_map.database.engine import engine, async_session
from alco_map.database.methods import add_store
from alco_map.database.models import Base, Store


@pytest.fixture
async def database():
    postgres_container = PostgresContainer("postgis/postgis:14-3.2-alpine", dbname="alco-map")
    postgres = postgres_container.start()
    connection_url = postgres.get_connection_url().replace("psycopg2", "asyncpg")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_add_store(database):
    address = "Ланское шоссе 228"
    image = "b64image"
    name = "Оранжевый"
    description = "Лучший на районе"
    lat = 228
    lon = 229

    await add_store(address,
                    image,
                    name,
                    description, lat, lon)

    async with async_session() as session:
        async with session.begin():
            stmt = select(Store)
            result = await session.execute(stmt)
            store = result.scalars().first()

            point = wkb.loads(bytes(store.coordinates.data))

            assert store.name == name
            assert store.image_b64 == image
            assert store.address == address
            assert store.description == description
            assert point.x == lat
            assert point.y == lon
