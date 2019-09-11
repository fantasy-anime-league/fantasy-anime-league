from fal.models import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fal.models import Team


class TeamWeeklyPoints(Base):
    __tablename__ = "team_weekly_points"

    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)
    team = relationship("Team", back_populates="team_weekly_points")
    week = Column(Integer, primary_key=True)
    weekly_points = Column(Integer, nullable=True)
    total_points = Column(Integer, nullable=True)
    is_highest = Column(Integer, default=0)

    def __repr__(self) -> str:
        return f'''In week {self.week}, {self.team.name} got {self.weekly_points}
            for a total of {self.total_points} for the season'''
