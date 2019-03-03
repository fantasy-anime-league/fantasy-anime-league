from fal.models import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Wildcard(Base):
    __tablename__ = 'wildcard'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    teams = relationship("WildcardUsage", back_populates="wildcard")
