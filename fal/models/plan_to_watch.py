from fal.models import Base

from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship


class PlanToWatch(Base):
    __tablename__ = 'plan_to_watch'

    anime_id = Column(Integer, ForeignKey('anime.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    count = Column(Integer)

    anime = relationship("Anime", back_populates='plan_to_watch')
