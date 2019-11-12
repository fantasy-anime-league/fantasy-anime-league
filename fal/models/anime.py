from typing import TYPE_CHECKING, TypeVar, Type, Set, Optional

import attr
import sqlalchemy.orm.exc

from fal.models import OrmFacade, Season
from fal import orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

T = TypeVar("T", bound=Anime)


@attr.s(frozen=True)
class Anime(OrmFacade):
    names: Set = attr.ib()
    restricted: bool = attr.ib(default=False)
    eligible: bool = attr.ib(default=True)

    @classmethod
    def get(cls: Type[T], name: str, session: Session) -> T:
        """
        Get anime from database based on name.

        Raises sqlalchemy.orm.exc.NoResultFound if no anime of that name found.
        Raises sqlalchemy.orm.exc.MultipleResultsFound if multiple object identities are returned,
        """

        try:
            orm_anime = session.query(orm.Anime).filter(orm.Anime.name == name).one()
        except sqlalchemy.orm.exc.NoResultFound:
            orm_anime = session.query(orm.Anime).filter(orm.Anime.alias == name).one()

        names = {orm_anime.name}
        if orm_anime.alias:
            names.add(orm_anime.alias)

        return cls(
            entity=orm_anime,
            session=session,
            names=names,
            restricted=orm_anime.restricted,
            eligible=orm_anime.eligible,
        )

    @classmethod
    def create(cls: Type[T], name: str, season: Season, session: Session) -> T
        """
        Adds new anime to database. Returns Anime object
        """
        assert isinstance(season._entity, orm.Season)