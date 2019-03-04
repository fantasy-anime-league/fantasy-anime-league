from fal.models import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fal.models import PlanToWatch, Season


class Anime(Base):
    __tablename__ = 'anime'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    season_id = Column(Integer, ForeignKey('season.id'))
    season = relationship("Season", baczk_populates='anime')
    sequel = Column(Boolean, default=0)
    eligible = Column(Boolean, nullable=True)
    alias = Column(String, nullable=True)

    plan_to_watch = relationship("PlanToWatch", back_populates='anime')

    def __repr__(self):
        return f"{self.name} - {self.id} from season id {self.season_id}"
