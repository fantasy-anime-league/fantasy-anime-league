import factory

from .session import session_factory
from .team import TeamFactory
from .anime import AnimeFactory
from fal.models import TeamWeeklyAnime


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
    ace = 0
    bench = 0

    team = factory.SubFactory(TeamFactory)
    anime = factory.SubFactory(AnimeFactory)
