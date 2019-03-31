from __future__ import annotations

from fal.models import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from fal.models import Anime, Team
    from sqlalchemy.orm import Session


class Season(Base):
    __tablename__ = 'season'

    id = Column(Integer, primary_key=True)
    season_of_year = Column(String)
    year = Column(Integer)

    anime = relationship("Anime", back_populates='season')
    teams = relationship("Team", back_populates='season')

    def __repr__(self) -> str:
        return f"id:{self.id} - {self.season_of_year} {self.year}"

    @staticmethod
    def get_season_from_database(season_of_year: str, year: int, session: Session) -> Season:
        """Adds the season to the Season table in the database if necessary, then returns Season object
        """

        query = session.query(Season).filter(
            Season.season_of_year == season_of_year,
            Season.year == year
        )
        current_season = query.one_or_none()

        if not current_season:
            current_season = Season(season_of_year=season_of_year, year=year)
            session.add(current_season)
            session.commit()

        return current_season
