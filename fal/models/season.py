from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, Generic, Iterator, Iterable, cast
from enum import Enum
import configparser

import attr

from .base import OrmFacade
import fal.models
import fal.orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

T = TypeVar("T", bound="Season")

config = configparser.ConfigParser()
config.read("config.ini")


class SeasonOfYear(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"


@attr.s(auto_attribs=True)
class Season(OrmFacade):
    _entity: fal.orm.Season
    season_of_year: SeasonOfYear
    year: int

    # TODO: move this field to db so we don't have to retrieve it from config file every time
    min_weeks_between_bench_swaps: int = config.getint(
        "season info", "min-weeks-between-bench-swaps"
    )

    def get_entity(self) -> fal.orm.Base:
        return self._entity

    @classmethod
    def from_orm_season(
        cls: Type[T], orm_season: fal.orm.Season, session: Session
    ) -> T:
        assert (
            orm_season.year is not None
        )  # sqlalchemy for some reason thinks name is optional

        return cls(
            entity=orm_season,
            session=session,
            season_of_year=SeasonOfYear(orm_season.season_of_year),
            year=orm_season.year,
        )

    @classmethod
    def get_or_create(
        cls: Type[T], season_of_year: SeasonOfYear, year: int, session: Session
    ) -> T:
        """
        Creates a new season in database if necessary, otherwise retrieves it. Returns Season object
        """

        query = session.query(fal.orm.Season).filter(
            fal.orm.Season.season_of_year == season_of_year.value,
            fal.orm.Season.year == year,
        )
        orm_season = query.one_or_none()

        if not orm_season:
            orm_season = fal.orm.Season(season_of_year=season_of_year.value, year=year)
            session.add(orm_season)
            session.commit()

        config.read("config.ini")

        return cls(
            session=session, entity=orm_season, season_of_year=season_of_year, year=year
        )

    def init_new_week(self, current_week: int) -> None:
        """
        Initializes this week with a new set of TeamWeeklyAnime,
        which is the first thing needed before doing other stuff with the week.

        Should fail in theory if you forget to change the week number in config.ini, since
        session.add() shouldn't clobber existing data
        """

        last_week_team_weekly_anime = (
            self._session.query(fal.orm.TeamWeeklyAnime, fal.orm.Team)
            .filter(
                fal.orm.TeamWeeklyAnime.week == current_week - 1,
                fal.orm.Team.season_id == self._entity.id,
                fal.orm.Team.id == fal.orm.TeamWeeklyAnime.team_id,
            )
            .all()
        )

        for team_weekly_anime, team in last_week_team_weekly_anime:
            new_team_weekly_anime = fal.orm.TeamWeeklyAnime(
                team_id=team.id,
                anime_id=team_weekly_anime.anime_id,
                week=current_week,
                bench=team_weekly_anime.bench,
            )
            self._session.add(new_team_weekly_anime)

        self.commit()

    def get_all_anime(self) -> Iterator[fal.models.Anime]:
        return (
            fal.models.Anime.from_orm_anime(anime, self._session)
            for anime in cast(Iterable[fal.orm.Anime], self._entity.anime)
        )

    def get_all_teams(self) -> Iterator[fal.models.Team]:
        return (
            fal.models.Team.from_orm_team(team, self._session)
            for team in cast(Iterable[fal.orm.Team], self._entity.teams)
        )
