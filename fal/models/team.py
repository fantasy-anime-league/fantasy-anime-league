from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, List
import configparser

from sqlalchemy import or_, func
import attr

from fal.models import OrmFacade, Anime
from fal import orm

if TYPE_CHECKING:
    from fal.models import Season
    from sqlalchemy.orm import Session

T = TypeVar("T", bound="Team")
config = configparser.ConfigParser()


@attr.s(frozen=True, auto_attribs=True)
class Team(OrmFacade):
    _entity: orm.Team
    name: str

    def get_entity(self) -> orm.Base:
        return self._entity

    @classmethod
    def get_by_name(cls: Type[T], name: str, season: Season, session: Session) -> T:
        """
        Get team from database based on name and season.

        Raises sqlalchemy.orm.exc.NoResultFound if no team of that name and season found.
        """
        orm_team = (
            session.query(orm.Team)
            .filter(orm.Team.name == name, orm.Team.season_id == season._entity.id)
            .one()
        )

        return cls(entity=orm_team, session=session, name=name)

    @classmethod
    def create(cls: Type[T], name: str, season: Season, session: Session) -> T:
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
        return cls(entity=orm_team, session=session, name=name)

    def bench_swap(self, active_anime: Anime, bench_anime: Anime, week: int) -> None:
        """
        Moves bench_anime to active and active_anime to bench.

        Raises if anime passed in are not actually active/bench.
        """

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

    def add_anime_to_team(self, anime: Anime, bench: bool = False) -> None:
        """
        Can only be called in week 0, adds anime to team's active or bench.

        Raises sqlalchemy.exc.IntegrityError if anime already exists on team.
        """
        config.read("config.ini")

        assert config.getint("weekly info", "current-week") == 0

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
                orm.TeamWeeklyAnime.week == week
            )
            .all()
        )

        snapshot = WeekSnapshotOfTeamAnime(week=week)
        for team_weekly_anime in this_week_anime:
            anime = Anime.from_orm_anime(team_weekly_anime.anime, self._session)
            if team_weekly_anime.bench:
                snapshot.bench.append(anime)
            else:
                snapshot.active.append(anime)

        return snapshot


@attr.s(auto_attribs=True)
class WeekSnapshotOfTeamAnime(object):
    week: int
    active: List[Anime] = attr.Factory(list)
    bench: List[Anime] = attr.Factory(list)