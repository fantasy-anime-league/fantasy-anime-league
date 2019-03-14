from fal.models import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fal.models import PlanToWatch, Season, AnimeWeeklyStat, TeamWeeklyAnime


class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    season_id = Column(Integer, ForeignKey("season.id"))
    season = relationship("Season", back_populates="anime")
    derivative = Column(Boolean, default=0)
    eligible = Column(Boolean, default=1)
    alias = Column(String, nullable=True)

    plan_to_watch = relationship("PlanToWatch", back_populates="anime")
    anime_weekly_stats = relationship(
        "AnimeWeeklyStat", back_populates="anime")
    team_weekly_anime = relationship("TeamWeeklyAnime", back_populates="anime")

    def __repr__(self):
        return f"{self.name} - {self.id} from season id {self.season_id}"
