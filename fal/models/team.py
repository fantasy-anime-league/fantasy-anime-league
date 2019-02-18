from fal.models import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    season_id = Column(String, ForeignKey('season.id'))
    season = relationship("Season", back_populates='teams')
    name = Column(String)
