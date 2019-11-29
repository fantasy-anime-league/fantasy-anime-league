from fal.orm import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fal.orm import Anime, Team


class BenchSwap(Base):
    __tablename__ = "bench_swap"

    team_id = Column(Integer, ForeignKey("team.id"), primary_key=True)
    team = relationship("Team")
    week = Column(Integer, primary_key=True)
    from_bench = Column(Integer, ForeignKey("anime.id"))
    to_bench = Column(Integer, ForeignKey("anime.id"))

    def __repr__(self) -> str:
        return f"""
            In week {self.week}, {self.team.name} put anime id {self.from_bench} on their active
            and {self.to_bench} on their bench
            """
