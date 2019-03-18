import factory

from .session import session_factory
from .season import SeasonFactory
import fal.models


class TeamFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = fal.models.Team
        sqlalchemy_session = session_factory

    id = factory.Sequence(lambda x: x)
    season_id = 1
    name = factory.Faker("user_name")

    season = factory.SubFactory(
        SeasonFactory, id=factory.SelfAttribute('..season_id'))
    # fill these out later
    wildcards = []
    team_weekly_anime = []
