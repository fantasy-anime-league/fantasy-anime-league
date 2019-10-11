from fal.models import Base

from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fal.models import Anime


class PlanToWatch(Base):
    __tablename__ = "plan_to_watch"

    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)
    date = Column(Date, primary_key=True)
    count = Column(Integer)

    anime = relationship("Anime", back_populates="plan_to_watch")

    def __repr__(self) -> str:
        return f"Anime id: {self.anime_id} - count: {self.count} on {self.date}"
