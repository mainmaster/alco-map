import pytest
from shapely import wkb
from sqlalchemy.future import select

from alco_map.database.models import Store


@pytest.mark.asyncio
async def test_add_store(db):
    address = "Ланское шоссе 228"
    image = "b64image"
    name = "Оранжевый"
    description = "Лучший на районе"
    lat = 228
    lon = 229

    await db.add_store(address,
                       image,
                       name,
                       description, lat, lon)

    async with db.session_factory() as session, session.begin():
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
