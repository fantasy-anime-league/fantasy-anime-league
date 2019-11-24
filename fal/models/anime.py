from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Type, Set, Optional, cast

import attr
import sqlalchemy.orm.exc

from fal.models import OrmFacade
from fal import orm

if TYPE_CHECKING:
    from fal.models import Season
    from sqlalchemy.orm import Session

T = TypeVar("T", bound="Anime")


@attr.s(auto_attribs=True)
class Anime(OrmFacade):
    _entity: orm.Anime
    mal_id: int
    names: Set[str]
    restricted: bool = False
    eligible: bool = True

    def get_entity(self) -> orm.Base:
        return self._entity

    @classmethod
    def get_by_name(cls: Type[T], name: str, session: Session) -> T:
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
    def from_orm_anime(cls: Type[T], orm_anime: orm.Anime, session: Session) -> T:
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
    def create(
        cls: Type[T], mal_id: int, name: str, season: Season, session: Session
    ) -> T:
        """
        Adds new anime to database. Returns Anime object.

        Raises sqlalchemy.exc.IntegrityError if anime already exists.
        """
        orm_anime = orm.Anime(id=mal_id, name=name, season_id=season._entity.id)
        session.add(orm_anime)
        session.commit()

        return cls(entity=orm_anime, session=session, mal_id=mal_id, names={name})

    def add_alias(self, alias: str) -> None:
        self.names.add(alias)
        self._entity.alias = alias
