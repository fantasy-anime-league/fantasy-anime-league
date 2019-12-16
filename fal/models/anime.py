from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, Set, Optional, cast, Dict
import functools

import attr
import sqlalchemy.orm.exc

from .base import OrmFacade
from fal import orm

if TYPE_CHECKING:
    from fal.models import Season
    from sqlalchemy.orm import Session


Anime_T = TypeVar("Anime_T", bound="Anime")


@attr.s(auto_attribs=True, kw_only=True, frozen=True)
class Anime(OrmFacade[orm.Anime]):
    _entity: orm.Anime
    mal_id: int
    names: Set[str]
    restricted: bool = False
    eligible: bool = True

    _anime_weekly_stat_cache: Dict[int, orm.AnimeWeeklyStat] = attr.Factory(dict)

    @classmethod
    def from_orm_anime(
        cls: Type[Anime_T], orm_anime: orm.Anime, session: Session
    ) -> Anime_T:
        """
        Conversion constructor from the orm class to our facade class
        """

        assert orm_anime.name  # sqlalchemy for some reason thinks name is optional
        names: Set[str] = {orm_anime.name}
        if orm_anime.alias:
            names.add(orm_anime.alias)

        return cls(
            entity=orm_anime,
            session=session,
            mal_id=orm_anime.id,
            names=names,
            restricted=orm_anime.restricted,
            eligible=orm_anime.eligible,
        )

    @classmethod
    @functools.lru_cache()
    def get_by_name(cls: Type[Anime_T], name: str, session: Session) -> Anime_T:
        """
        Get anime from database based on name.

        Raises sqlalchemy.orm.exc.NoResultFound if no anime of that name found.
        Raises sqlalchemy.orm.exc.MultipleResultsFound if multiple object identities are returned.
        """

        try:
            orm_anime = session.query(orm.Anime).filter(orm.Anime.name == name).one()
        except sqlalchemy.orm.exc.NoResultFound:
            orm_anime = session.query(orm.Anime).filter(orm.Anime.alias == name).one()

        return cls.from_orm_anime(orm_anime, session)

    @classmethod
    def create(
        cls: Type[Anime_T], mal_id: int, name: str, season: Season, session: Session
    ) -> Anime_T:
        """
        Adds new anime to database. Returns Anime object.

        Raises sqlalchemy.exc.IntegrityError if anime already exists.
        """
        orm_anime = orm.Anime(id=mal_id, name=name, season_id=season._entity.id)
        session.add(orm_anime)
        session.commit()

        return cls(entity=orm_anime, session=session, mal_id=mal_id, names={name})

    def get_forum_posts_for_week(self, week: int) -> int:
        total_forum_posts = self._get_anime_weekly_stat(week).total_forum_posts
        assert total_forum_posts  # because sqlalchemy thinks this is Optional for some reason
        return total_forum_posts

    def add_alias(self, alias: str) -> None:
        self.names.add(alias)
        self.entity.alias = alias

    def _get_anime_weekly_stat(self, week: int) -> orm.AnimeWeeklyStat:
        if anime_weekly_stat := self._anime_weekly_stat_cache.get(week):
            assert anime_weekly_stat  # mypy bug
            return anime_weekly_stat

        return (
            self._session.query(orm.AnimeWeeklyStat)
            .filter(
                orm.AnimeWeeklyStat.week == week,
                orm.AnimeWeeklyStat.anime_id == self.entity.id,
            )
            .one()
        )
