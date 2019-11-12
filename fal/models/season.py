from typing import TYPE_CHECKING, TypeVar, Type, Generic

import attr

from fal.models import OrmFacade
from fal import orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

T = TypeVar("T", bound=Season)


@attr.s(frozen=True, auto_attribs=True)
class Season(OrmFacade):
    _entity: orm.Season
    season_of_year: str
    year: int

    def get_entity(self) -> orm.Base:
        return self._entity

    @classmethod
    def get_or_create(
        cls: Type[T], season_of_year: str, year: int, session: Session
    ) -> T:
        """
        Creates a new season in database if necessary, otherwise retrieves it. Returns Season object
        """

        query = session.query(orm.Season).filter(
            orm.Season.season_of_year == season_of_year, orm.Season.year == year
        )
        orm_season = query.one_or_none()

        if not orm_season:
            orm_season = orm.Season(season_of_year=season_of_year, year=year)
            session.add(orm_season)
            session.commit()

        return cls(
            session=session,
            entity=orm_season,
            season_of_year=season_of_year,
            year=year,
        )
