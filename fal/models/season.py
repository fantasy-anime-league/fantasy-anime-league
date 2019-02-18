from fal.models import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Season(Base):
    __tablename__ = 'season'

    id = Column(Integer, primary_key=True)
    season_of_year = Column(String)
    year = Column(Integer)

    anime = relationship("Anime", back_populates='season')
    teams = relationship("Team", back_populates='season')
