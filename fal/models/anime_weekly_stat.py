from fal.models import Base

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fal.models import Anime


class AnimeWeeklyStat(Base):
    __tablename__ = "anime_weekly_stat"

    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)
    anime = relationship("Anime", back_populates="anime_weekly_stats")
    week = Column(Integer, primary_key=True)
    watching = Column(Integer)
    completed = Column(Integer)
    dropped = Column(Integer)
    score = Column(Float)
    favorites = Column(Integer)
