from .engine import async_session
from .models import Store


async def get_nearest_stores(current_address):
    pass


async def add_store(address, image_b64, name, description, latitude, longitude):
    """
    :param address: Store address (Alco street 33)
    :param image_b64: Store image in b64
    :param name: Store name (ex - Продукты 24)
    :param description: Store description (ex - Лучший магазин на районе)
    :param latitude: Store latitude
    :param longitude: Store longitude
    :return:
    """
    coordinates = f"POINT({latitude} {longitude})"
    store = Store(address=address,
                  image_b64=image_b64,
                  name=name,
                  description=description,
                  coordinates=coordinates)

    async with async_session() as session:
        async with session.begin():
            session.add(store)


async def add_like(store_id, user_from=None, positive=True):
    pass


async def get_likes(store_id):
    pass
