from typing import Iterable

from cock import Option, build_options_from_dict
from facet import ServiceMixin
from geoalchemy2 import func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from yarl import URL

from alco_map.database.models import Base, Store
from alco_map.injector import inject, register


class Database(ServiceMixin):

    def __init__(self, connection_url):
        self.connection_url = connection_url
        self.engine = None
        self.session_factory = None

    async def start(self):
        self.engine = create_async_engine(self.connection_url, echo=True)
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        self.session_factory = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def get_nearest_stores(self, latitude: float, longitude: float) -> Iterable[Store]:
        """
        Get nearest store by coordinates

        :param latitude: Store latitude
        :param longitude: Store longitude
        :return:
        """
        async with self.session_factory() as session, session.begin():
            point = func.ST_GeomFromText(f"POINT({longitude} {latitude})", 27700)
            query = select(Store, func.ST_Distance(Store.coordinates, point)
                           .label('distance')) \
                .order_by('distance') \
                .limit(10)
            result = await session.execute(query)
            return result.scalars()

    async def add_store(self, address: str, image_b64: str, name: str, description: str, latitude: float,
                        longitude: float) -> None:
        """
        Add new store

        :param address: Store address (Alco street 33)
        :param image_b64: Store image in b64
        :param name: Store name (ex - Продукты 24)
        :param description: Store description (ex - Лучший магазин на районе)
        :param latitude: Store latitude
        :param longitude: Store longitude
        :return:
        """
        coordinates = f"POINT({longitude} {latitude})"
        store = Store(address=address,
                      image_b64=image_b64,
                      name=name,
                      description=description,
                      coordinates=coordinates)

        async with self.session_factory() as session, session.begin():
            session.add(store)

    async def add_like(self, store_id, user_from=None, positive=True):
        pass

    async def get_likes(self, store_id):
        pass


@register(name="database", singleton=True)
@inject
def database_from_config(config):
    url = URL.build(
        scheme="postgresql+asyncpg",
        user=config.db_user,
        password=config.db_password,
        host=config.db_host,
        port=config.db_port,
        path="/" + config.db_database,
    )
    return Database(connection_url=str(url))


database_options = build_options_from_dict({
    "db": {
        "host": Option(default="db"),
        "port": Option(default=5432, type=int),
        "user": Option(default="postgres"),
        "password": Option(default="admin"),
        "database": Option(required=True),
    }
})
