from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type

from sqlalchemy import or_
import attr

from fal.models import OrmFacade
from fal import orm

if TYPE_CHECKING:
    from fal.models import Season, Anime
    from sqlalchemy.orm import Session

T = TypeVar("T", bound="Team")


@attr.s(frozen=True, auto_attribs=True)
class Team(OrmFacade):
    _entity: orm.Team
    name: str

    def get_entity(self) -> orm.Base:
        return self._entity

    @classmethod
    def get_or_create(cls: Type[T], name: str, season: Season, session: Session) -> T:
        """
        Creates a new team in database if necessary, otherwise retrieves it. Returns Team object
        """

        orm_team = (
            session.query(orm.Team)
            .filter(orm.Team.name == name, orm.Team.season_id == season._entity.id)
            .query.one_or_none()
        )

        if not orm_team:
            team = orm_team.Team(name=name, season_id=season._entity.id)
            session.add(orm_team)
            session.commit()

        return cls(entity=orm_team, session=session, name=name)

    def bench_swap(self, active_anime: Anime, bench_anime: Anime, week: int) -> None:
        """
        Moves bench_anime to active and active_anime to bench.

        Raises if anime passed in are not actually active/bench.
        """

        this_week_anime = (
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

        assert len(this_week_anime) == 2

        for anime in this_week_anime:
            if anime.anime_id == active_anime._entity.id:
                assert not anime.bench
                anime.bench = 1
            elif anime.anime_id == bench_anime._entity.id:
                assert anime.bench
                anime.bench = 0
