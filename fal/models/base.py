import attr

import abc
from typing import TYPE_CHECKING, TypeVar, Generic

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from fal.orm import Base

T = TypeVar("T", bound=Base)


@attr.s
class OrmFacade(abc.ABC, Generic[T]):
    _entity: T = attr.ib()
    _session: Session = attr.ib()

    def commit(self) -> None:
        self._session.commit()
