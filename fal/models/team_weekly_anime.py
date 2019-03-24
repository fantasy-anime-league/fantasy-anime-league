from fal.models import Base

from sqlalchemy import Column, Integer, Boolean, ForeignKey
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
    ace = Column(Boolean, default=False)
    bench = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'''In week {self.week}, {self.team.name} has {self.anime.name} on their team.'
                    Bench: {self.bench}, Ace: {self.ace}'''
