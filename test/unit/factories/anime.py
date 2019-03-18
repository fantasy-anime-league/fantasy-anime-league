import factory

from .session import session_factory
from .season import SeasonFactory
import fal.models


class AnimeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = fal.models.Anime
        sqlalchemy_session = session_factory

    id = factory.Sequence(lambda x: x)
    name = factory.Faker('sentence', nb_words=6, variable_nb_words=True)
    season_id = 1
    season = factory.SubFactory(
        SeasonFactory, id=factory.SelfAttribute('..season_id'))
    derivative = factory.Faker('random_int', min=0, max=1)
    eligible = factory.Faker('random_int', min=0, max=1)
    alias = None

    # fill these out later
    plan_to_watch = []
    anime_weekly_stats = []
    team_weekly_anime = []
