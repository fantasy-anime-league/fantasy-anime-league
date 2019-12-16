from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Generic, TypeVar

import attr

if TYPE_CHECKING:
    from fal import orm
    from sqlalchemy.orm import Session


OrmBase_T = TypeVar("OrmBase_T", bound="orm.Base", covariant=True)


@attr.s(auto_attribs=True, kw_only=True)
class OrmFacade(Generic[OrmBase_T], abc.ABC):
    """
    Instances of OrmFacade should be the only ones accessing the ORM layer.
    They should also generally not contain any business logic,
    e.g. knowledge of the state of the config

    Generally these will be the interface that controllers will access.
    """

    _entity: OrmBase_T
    _session: Session

    def commit(self) -> None:
        self._session.commit()

    @property
    def entity(self) -> OrmBase_T:
        """
        Entity in general should not be directly accessed anywhere outside of child classes of OrmFacade
        """
        return self._entity
