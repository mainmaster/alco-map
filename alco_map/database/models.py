from geoalchemy2.types import Geometry
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    image_b64 = Column(String, default=None)
    coordinates = Column(Geometry(geometry_type="POINT", srid=27700))


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"), primary_key=True)
    positive = Column(Boolean)
    user_from = Column(String, default=None)


class SearchHistory(Base):
    __tablename__ = "search_history"
    id = Column(Integer, primary_key=True)
    address = Column(String, default=None)
    coordinates = Column(Geometry(geometry_type="POINT", srid=27700), default=None)
