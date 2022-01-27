import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class DBConnector:
    connection_url = ""

    def __init__(self):
        host = os.getenv("ALCO_MAP_DB_HOST")
        user = os.getenv("ALCO_MAP_DB_USER")
        password = os.getenv("ALCO_MAP_DB_PASS")
        db_name = os.getenv("ALCO_MAP_DB_NAME")

        connection_url = f"postgresql+asyncpg://{user}:{password}@{host}/{db_name}"
        self.connection_url = connection_url

    @property
    def engine(self):
        engine = create_async_engine(
            self.connection_url, echo=True,
        )
        return engine

    @property
    def session(self):
        async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        return async_session
