import pytest

from database.models import Base
from database.engine import engine
from database.methods import add_store

@pytest.fixture
async def database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_add_store(database):
    pass
