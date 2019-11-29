from fal.orm import Base

from sqlalchemy import Column, Integer, String


class Secret(Base):
    __tablename__ = "secret"

    key = Column(String, primary_key=True)
    value = Column(String)
    context = Column(String, primary_key=True, nullable=True)
