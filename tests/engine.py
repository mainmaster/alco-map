from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

postgres_container = PostgresContainer("postgis/postgis:14-3.2-alpine", dbname="alco-map")
postgres = postgres_container.start()
connection_url = postgres.get_connection_url().replace("psycopg2", "asyncpg")
print(connection_url)

engine = create_async_engine(connection_url, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
