from typing import TYPE_CHECKING, TypeVar, Type

import attr

from fal.models import OrmFacade, Season
from fal import orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

T = TypeVar("T", bound=Team)


@attr.s(frozen=True)
class Team(OrmFacade):
    name: str = attr.ib()

    @classmethod
    def get_or_create(cls: Type[T], name: str, season: Season, session: Session) -> T:
        """
        Creates a new team in database if necessary, otherwise retrieves it. Returns Team object
        """

        assert isinstance(season._entity, orm.Season)
        query = session.query(orm.Team).filter(
            orm.Team.name == name, orm.Team.season_id == season._entity.id
        )
        orm_team = query.one_or_none()

        if not orm_team:
            team = orm_team.Team(name=name, season_id=season._entity.id)
            session.add(orm_team)
            session.commit()

        return cls(entity=orm_team, session=session, name=name)
