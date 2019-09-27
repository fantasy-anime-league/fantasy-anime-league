from fal.models import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fal.models import Anime, Team


class TeamWeeklyAnime(Base):
    __tablename__ = "team_weekly_anime"

    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)
    team = relationship("Team", back_populates="team_weekly_anime")
    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)
    anime = relationship("Anime")
    week = Column(Integer, primary_key=True)
    ace = Column(Integer, default=0)
    bench = Column(Integer, default=0)

    def __repr__(self) -> str:
        return f'In week {self.week}, {self.team.name} has {self.anime.name} on their team.' \
               f'Bench: {self.bench}, Ace: {self.ace}'
