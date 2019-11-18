from __future__ import annotations

import abc
from typing import TYPE_CHECKING

import attr

if TYPE_CHECKING:
    from fal import orm
    from sqlalchemy.orm import Session


@attr.s(auto_attribs=True)
class OrmFacade(abc.ABC):
    _session: Session

    def commit(self) -> None:
        self._session.commit()

    @abc.abstractmethod
    def get_entity(self) -> orm.Base:
        """
        _entity in general should not be directly accessed anywhere outside of child classes of OrmFacade
        """
        pass
