from fal.models import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fal.models import Anime, Team


class Season(Base):
    __tablename__ = 'season'

    id = Column(Integer, primary_key=True)
    season_of_year = Column(String)
    year = Column(Integer)

    anime = relationship("Anime", back_populates='season')
    teams = relationship("Team", back_populates='season')

    def __repr__(self):
        return f"{self.season_of_year} {self.year}"
