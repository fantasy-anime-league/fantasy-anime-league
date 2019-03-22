import factory

from .session import session_factory
from .season import SeasonFactory
from fal.models import Season, Anime


class AnimeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Anime
        sqlalchemy_session = session_factory

    id = factory.Sequence(lambda x: x)
    name = factory.Faker('sentence', nb_words=6, variable_nb_words=True)
    season_id = 0
    derivative = factory.Faker('random_int', min=0, max=1)
    eligible = factory.Faker('random_int', min=0, max=1)
    alias = None

    @factory.lazy_attribute
    def season(self):
        return session_factory().query(Season).filter(Season.id == self.season_id).one()

    # fill these out later
    plan_to_watch = []
    anime_weekly_stats = []
    team_weekly_anime = []
