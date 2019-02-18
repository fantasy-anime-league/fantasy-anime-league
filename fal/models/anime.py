from fal.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean


class Anime(Base):
    __tablename__ = 'anime'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    season = Column(Integer)
    sequel = Column(Boolean)
    alias = Column(String, nullable=True)
