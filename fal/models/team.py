from __future__ import annotations

from fal.models import Base, Season

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fal.models import Season, WildcardUsage, TeamWeeklyAnime
    from sqlalchemy.orm import Session


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    season_id = Column(String, ForeignKey('season.id'))
    name = Column(String)

    season = relationship("Season", back_populates="teams")
    wildcards = relationship("WildcardUsage", back_populates="team")
    team_weekly_anime = relationship("TeamWeeklyAnime", back_populates="team")

    @staticmethod
    def get_team_from_database(name: str, season: Season, session: Session) -> Team:
        """ Adds new team row to database if necessary, then return the team object"""
        query = session.query(Team).filter(
            Team.name == name,
            Team.season_id == season.id
        )
        team = query.one_or_none()

        if not team:
            team = Team(name=name, season_id=season.id)
            session.add(team)
            session.commit()
            query = session.query(Team).filter(
                Team.name == name,
                Team.season_id == season.id
            )
            team = query.one()

        return team

    def __repr__(self):
        return f'{self.id}: {self.name} from season {self.season_id}'
