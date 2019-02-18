from fal.models import Base
from sqlalchemy import Column, Integer, String


class Wildcard(Base):
    __tablename__ = 'wildcard'

    id = Column(Integer, primary_key=True)
    type = Column(String)
