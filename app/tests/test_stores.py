import pytest

from database.models import Base
from database.engine import engine


@pytest.fixture
async def database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_create_store(database):
    pass
