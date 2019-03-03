from fal.models import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Anime(Base):
    __tablename__ = 'anime'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    season_id = Column(String, ForeignKey('season.id'))
    season = relationship("Season", back_populates='anime')
    sequel = Column(Boolean)
    eligible = Column(Boolean, nullable=True)
    alias = Column(String, nullable=True)

    plan_to_watch = relationship("PlanToWatch", back_populates='anime')
