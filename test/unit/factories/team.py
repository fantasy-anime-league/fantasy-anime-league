import factory

from .session import session_factory
from .season import SeasonFactory
from fal.models import Season, Team


class TeamFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Team
        sqlalchemy_session = session_factory

    id = factory.Sequence(lambda x: x)
    season_id = 0
    name = factory.Faker("user_name")

    @factory.lazy_attribute
    def season(self):
        return session_factory().query(Season).filter(Season.id == self.season_id).one()

    # fill these out later
    wildcards = []
    team_weekly_anime = []
