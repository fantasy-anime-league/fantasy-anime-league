from fal.models import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fal.models import Team, Wildcard


class WildcardUsage(Base):
    __tablename__ = "wildcard_usage"

    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)
    wildcard_id = Column(Integer, ForeignKey("wildcard.id"), primary_key=True)
    week = Column(Integer)

    team = relationship("Team", back_populates="wildcards")
    wildcard = relationship("Wildcard", back_populates="teams")
