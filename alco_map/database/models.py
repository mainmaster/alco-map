from geoalchemy2.shape import to_shape
from geoalchemy2.types import Geometry
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    image_b64 = Column(String, default=None)
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326))

    def get_location(self) -> dict:
        point = to_shape(self.coordinates)
        return {
            "latitude": point.y,
            "longitude": point.x,
        }


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
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326), default=None)
