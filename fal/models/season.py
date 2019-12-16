from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, Generic, Iterator, Iterable, cast
from enum import Enum
import configparser

import attr

from . import OrmFacade
from fal import orm, models

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


@attr.s(auto_attribs=True, kw_only=True, frozen=True)
class Season(OrmFacade[orm.Season]):
    _entity: orm.Season
    season_of_year: SeasonOfYear
    year: int

    # TODO: move this field to db so we don't have to retrieve it from config file every time
    min_weeks_between_bench_swaps: int = config.getint(
        "season info", "min-weeks-between-bench-swaps"
    )


    @classmethod
    def from_orm_season(
        cls: Type[T], orm_season: orm.Season, session: Session
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

        query = session.query(orm.Season).filter(
            orm.Season.season_of_year == season_of_year.value,
            orm.Season.year == year,
        )
        orm_season = query.one_or_none()

        if not orm_season:
            orm_season = orm.Season(season_of_year=season_of_year.value, year=year)
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
            self._session.query(orm.TeamWeeklyAnime, orm.Team)
            .filter(
                orm.TeamWeeklyAnime.week == current_week - 1,
                orm.Team.season_id == self.entity.id,
                orm.Team.id == orm.TeamWeeklyAnime.team_id,
            )
            .all()
        )

        for team_weekly_anime, team in last_week_team_weekly_anime:
            new_team_weekly_anime = orm.TeamWeeklyAnime(
                team_id=team.id,
                anime_id=team_weekly_anime.anime_id,
                week=current_week,
                bench=team_weekly_anime.bench,
            )
            self._session.add(new_team_weekly_anime)

        self.commit()

    def get_all_anime(self) -> Iterator[models.Anime]:
        return (
            models.Anime.from_orm_anime(anime, self._session)
            for anime in cast(Iterable[orm.Anime], self.entity.anime)
        )

    def get_all_teams(self) -> Iterator[models.Team]:
        return (
            models.Team.from_orm_team(team, self._session)
            for team in cast(Iterable[orm.Team], self.entity.teams)
        )
