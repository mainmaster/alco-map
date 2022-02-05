import datetime
from typing import Iterable, List, Union

from cock import Option, build_options_from_dict
from facet import ServiceMixin
from geoalchemy2 import func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from yarl import URL

from alco_map.database.models import Base, Store, Like, SearchHistory
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

    async def get_nearest_stores(self, latitude: float, longitude: float, user_from: str | None = None) -> \
            Iterable[Store]:
        """
        Get nearest store by coordinates

        :param latitude: Store latitude
        :param longitude: Store longitude
        :param user_from: User ID or Nickname
        :return:
        """
        async with self.session_factory() as session, session.begin():
            point = f"POINT({longitude} {latitude})"
            coordinates = func.ST_GeomFromText(point, 4326)
            query = select(Store, func.ST_Distance(Store.coordinates, coordinates)
                           .label('distance')) \
                .order_by("distance") \
                .limit(10)
            result = await session.execute(query)
            session.add(SearchHistory(user_from=user_from, coordinates=coordinates))
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

    async def add_like(self, store_id: id, user_from: str = None, positive: bool = True) -> bool:
        """
        Vote for the store
        One user cannot upvote twice positively or twice negatively within 3 hours

        :param store_id: Store ID
        :param user_from: User ID or Nickname who gave the rating
        :param positive: True or False (positive or negative reaction)
        :return: boolean: False - vote not counted, True - vote counted
        """

        like = Like(store_id=store_id,
                    user_from=user_from,
                    positive=positive)

        async with self.session_factory() as session, session.begin():
            query = select(Like).where(Like.user_from == user_from,
                                       Like.store_id == store_id,
                                       Like.like_datetime > datetime.datetime.utcnow() - datetime.timedelta(hours=3))
            result = await session.execute(query)
            if result.scalars().first():
                return False
            session.add(like)
        return True

    async def get_likes(self, store_id: int) -> list[int]:
        """
        Get negative and positive likes

        :param store_id: Store ID
        :return: List with negative and positive likes count, ex [10, 5], 10 - negative, 5 - positive
        """
        async with self.session_factory() as session, session.begin():
            query = select(func.count(Like.positive)) \
                .where(Like.store_id == store_id) \
                .group_by(Like.positive).order_by(Like.positive)
            result = await session.execute(query)
            return result.scalars().all()


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
