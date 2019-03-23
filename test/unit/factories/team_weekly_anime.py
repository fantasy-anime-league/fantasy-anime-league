import factory

from .session import session_factory
from fal.models import TeamWeeklyAnime, Team, Anime


class TeamWeeklyAnimeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = TeamWeeklyAnime
        sqlalchemy_session = session_factory

    @factory.lazy_attribute
    def team_id(self):
        return self.team.id

    @factory.lazy_attribute
    def anime_id(self):
        return self.anime.id

    week = 0
    ace = False
    bench = False

    team = []
    anime = []
