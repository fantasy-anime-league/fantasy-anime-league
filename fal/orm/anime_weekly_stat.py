from fal.orm import Base

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fal.orm import Anime


class AnimeWeeklyStat(Base):
    __tablename__ = "anime_weekly_stat"

    anime_id = Column(Integer, ForeignKey("anime.id"), primary_key=True)
    anime = relationship("Anime", back_populates="anime_weekly_stats")
    week = Column(Integer, primary_key=True)
    watching = Column(Integer)
    completed = Column(Integer)
    dropped = Column(Integer)
    score = Column(Float, nullable=True)
    favorites = Column(Integer)
    forum_posts = Column(Integer)
    total_points = Column(Integer, default=0)

    def __repr__(self) -> str:
        return f"""
            {self.anime.name}:
                Watching - {self.watching}
                Completed - {self.completed}
                Dropped - {self.dropped}
                Score - {self.score}
                Favorites - {self.favorites}
                Forum Posts - {self.forum_posts}
                Total Points - {self.total_points}
            """
