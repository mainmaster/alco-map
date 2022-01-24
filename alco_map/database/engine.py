import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DB_HOST = os.getenv("ALCO_MAP_DB_HOST")
DB_USER = os.getenv("ALCO_MAP_DB_USER")
DB_PASS = os.getenv("ALCO_MAP_DB_PASSWORD")
DB_NAME = os.getenv("ALCO_MAP_DB_DATABASE")

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}", echo=True,
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
