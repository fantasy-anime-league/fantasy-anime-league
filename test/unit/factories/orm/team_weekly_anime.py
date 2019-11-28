import factory

from .session import session_factory
from .team import OrmTeamFactory
from .anime import OrmAnimeFactory
from fal.orm import TeamWeeklyAnime


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

    team = factory.SubFactory(OrmTeamFactory)
    anime = factory.SubFactory(OrmAnimeFactory)
