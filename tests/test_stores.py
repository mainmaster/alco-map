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
        assert point.x == lon
        assert point.y == lat


@pytest.mark.asyncio
async def test_get_nearest_stores(db):
    my_coord = ("59.996852", "30.323844",)
    test_data = [
        ("Ланское шоссе 3", "b64image", "Оранжевый3", "Лучший на районе3", 59.989931, 30.302680,),
        ("Ланское шоссе 1", "b64image", "Оранжевый1", "Лучший на районе1", 59.995186, 30.318627,),
        ("Ланское шоссе 2", "b64image", "Оранжевый2", "Лучший на районе2", 59.992483, 30.308879,)
    ]

    test_stores = []
    for store_data in test_data:
        coordinates = f"POINT({store_data[5]} {store_data[4]})"
        store = Store(address=store_data[0],
                      image_b64=store_data[1],
                      name=store_data[2],
                      description=store_data[3],
                      coordinates=coordinates)
        test_stores.append(store)

    async with db.session_factory() as session, session.begin():
        session.add_all(test_stores)

    result = await db.get_nearest_stores(my_coord[0], my_coord[1])
    result_stores = [store for store in result]

    assert result_stores[0].name == test_data[1][2]
    assert result_stores[1].name == test_data[2][2]
    assert result_stores[2].name == test_data[0][2]

    location = result_stores[0].get_location()
    assert location == {
        "latitude": test_data[1][4],
        "longitude": test_data[1][5],
    }
