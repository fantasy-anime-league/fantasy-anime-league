from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, List

from sqlalchemy import or_, func, desc
import attr

from .base import OrmFacade
import fal.models
from fal import orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

T = TypeVar("T", bound="Team")


@attr.s(frozen=True, auto_attribs=True)
class Team(OrmFacade):
    _entity: orm.Team
    name: str
    season: fal.models.Season

    def get_entity(self) -> orm.Base:
        return self._entity

    @classmethod
    def from_orm_team(cls: Type[T], orm_team: orm.Team, session: Session) -> T:
        """
        Conversion constructor from the orm class to our facade class
        """
        assert orm_team.name  # sqlalchemy for some reason thinks name is optional
        return cls(
            entity=orm_team,
            session=session,
            name=orm_team.name,
            season=fal.models.Season.from_orm_season(orm_team.season, session),
        )

    @classmethod
    def get_by_name(cls: Type[T], *, name: str, season: fal.models.Season, session: Session) -> T:
        """
        Get team from database based on name and season.

        Raises sqlalchemy.orm.exc.NoResultFound if no team of that name and season found.
        """
        orm_team = (
            session.query(orm.Team)
            .filter(orm.Team.name == name, orm.Team.season_id == season._entity.id)
            .one()
        )

        return cls(entity=orm_team, session=session, name=name, season=season)

    @classmethod
    def create(cls: Type[T], *, name: str, season: fal.models.Season, session: Session) -> T:
        """
        Adds new team to database. Returns Team object.

        Raises AssertionError if team already exists.
        """
        assert not (
            session.query(func.count(orm.Team.id))
            .filter(orm.Team.name == name, orm.Team.season_id == season._entity.id)
            .scalar()
        )
        orm_team = orm.Team(name=name, season_id=season._entity.id)
        session.add(orm_team)
        session.commit()
        return cls(entity=orm_team, session=session, name=name, season=season)

    def bench_swap(self, *, active_anime: fal.models.Anime, bench_anime: fal.models.Anime, week: int) -> None:
        """
        Moves bench_anime to active and active_anime to bench.

        Raises if anime passed in are not actually active/bench.
        Raises if the number of weeks since the last bench swap is less than
        'min-weeks-between-bench-swaps' from config.ini
        """

        last_bench_swap_week_row = (
            self._session.query(orm.BenchSwap.week)
            .filter(orm.BenchSwap.team_id == self._entity.id)
            .order_by(desc(orm.BenchSwap.week))
            .first()
        )

        if last_bench_swap_week_row:
            last_bench_swap_week = last_bench_swap_week_row.week
            assert (
                week - last_bench_swap_week >= self.season.min_weeks_between_bench_swaps
            )

        this_week_anime_involved = (
            self._session.query(orm.TeamWeeklyAnime)
            .filter(
                orm.TeamWeeklyAnime.team_id == self._entity.id,
                orm.TeamWeeklyAnime.week == week,
                or_(
                    orm.TeamWeeklyAnime.anime_id == active_anime._entity.id,
                    orm.TeamWeeklyAnime.anime_id == bench_anime._entity.id,
                ),
            )
            .all()
        )

        assert len(this_week_anime_involved) == 2

        for anime in this_week_anime_involved:
            if anime.anime_id == active_anime._entity.id:
                assert not anime.bench
                anime.bench = 1
            elif anime.anime_id == bench_anime._entity.id:
                assert anime.bench
                anime.bench = 0

        successful_swap = orm.BenchSwap(
            team_id=self._entity.id,
            week=week,
            to_bench=active_anime._entity.id,
            from_bench=bench_anime._entity.id,
        )
        self._session.add(successful_swap)
        self.commit()

    def add_anime_to_team(self, anime: fal.models.Anime, bench: bool = False) -> None:
        """
        Should only be called in week 0, adds anime to team's active or bench.

        Raises sqlalchemy.exc.IntegrityError if anime already exists on team.
        """
        first_week_anime = orm.TeamWeeklyAnime(
            team_id=self._entity.id,
            anime_id=anime._entity.id,
            week=0,
            bench=int(bench),
        )
        self._session.add(first_week_anime)
        self.commit()

    def get_anime(self, week: int) -> WeekSnapshotOfTeamAnime:
        """
        Returns all anime on team during week specified
        """
        this_week_anime = (
            self._session.query(orm.TeamWeeklyAnime)
            .filter(
                orm.TeamWeeklyAnime.team_id == self._entity.id,
                orm.TeamWeeklyAnime.week == week,
            )
            .all()
        )

        snapshot = WeekSnapshotOfTeamAnime(week=week)
        for team_weekly_anime in this_week_anime:
            anime = fal.models.Anime.from_orm_anime(team_weekly_anime.anime, self._session)
            if team_weekly_anime.bench:
                snapshot.bench.append(anime)
            else:
                snapshot.active.append(anime)

        return snapshot


@attr.s(auto_attribs=True)
class WeekSnapshotOfTeamAnime(object):
    week: int
    active: List[fal.models.Anime] = attr.Factory(list)
    bench: List[fal.models.Anime] = attr.Factory(list)