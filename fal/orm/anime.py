from __future__ import annotations

from fal.orm import Base
from fal.utils import deprecated

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

import functools
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from fal.orm import PlanToWatch, Season, AnimeWeeklyStat, TeamWeeklyAnime
    from sqlalchemy.orm import relationship, Session


class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    season_id = Column(Integer, ForeignKey("season.id"))
    season = relationship("Season", back_populates="anime")
    restricted = Column(Boolean, default=0)
    eligible = Column(Boolean, default=1)
    alias = Column(String, nullable=True)

    plan_to_watch = relationship("PlanToWatch", back_populates="anime")
    anime_weekly_stats = relationship("AnimeWeeklyStat", back_populates="anime")
    team_weekly_anime = relationship("TeamWeeklyAnime", back_populates="anime")

    def __repr__(self) -> str:
        return f"{self.name} - {self.id} from season id {self.season_id}"

    @staticmethod
    @deprecated("use models.anime.create instead")
    def add_anime_to_database(
        id: int, name: str, season: Season, session: Session
    ) -> None:
        """
        Adds new anime row to database if it doesn't already exist
        """
        query = session.query(Anime).filter(Anime.id == id)
        anime = query.one_or_none()

        if anime:
            print(f"{anime} already exists in database")
        else:
            anime = Anime(id=id, name=name, season_id=season.id)
            print(f"Adding {anime} to database")
            session.add(anime)

    @staticmethod
    @functools.lru_cache(maxsize=64)
    @deprecated("use models.anime.get instead")
    def get_anime_from_database_by_name(name: str, session: Session) -> Optional[Anime]:
        """
        Get anime from database based on name. Return None if it's not there.
        """
        query = session.query(Anime).filter(Anime.name == name)
        anime = query.one_or_none()

        return anime
