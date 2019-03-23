import factory

from .session import session_factory
from fal.models import TeamWeeklyAnime, Team


class TeamWeeklyAnimeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = TeamWeeklyAnime
        sqlalchemy_session = session_factory

    team_id = factory.Sequence(lambda x: x)
    anime_id = factory.Faker('random_int', min=35000, max=40000)
    week = 0
    ace = False
    bench = False

    @factory.lazy_attribute
    def team(self):
        return session_factory().query(Team).filter(Team.id == self.team_id).one()

    # fill it out later
    anime = []
