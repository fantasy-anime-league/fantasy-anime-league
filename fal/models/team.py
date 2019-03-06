from fal.models import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fal.models import Season, WildcardUsage, TeamWeeklyAnime


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    season_id = Column(String, ForeignKey('season.id'))
    name = Column(String)

    season = relationship("Season", back_populates="teams")
    wildcards = relationship("WildcardUsage", back_populates="team")
    team_weekly_anime = relationship("TeamWeeklyAnime", back_populates="team")
