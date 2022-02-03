from geoalchemy2.types import Geometry
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    image_b64 = Column(String, default=None)
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326))


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey("stores.id"), primary_key=True)
    positive = Column(Boolean)
    like_datetime = Column(DateTime, default=datetime.now())
    user_from = Column(String, default=None, index=True)


class SearchHistory(Base):
    __tablename__ = "search_history"
    id = Column(Integer, primary_key=True)
    query_datetime = Column(DateTime, default=datetime.now())
    user_from = Column(String, default=None)
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326), default=None)
