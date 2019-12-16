import factory

from .session import session_factory
from .anime import OrmAnimeFactory
from fal.orm import AnimeWeeklyStat


class AnimeWeeklyStatFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = AnimeWeeklyStat
        sqlalchemy_session = session_factory

    @factory.lazy_attribute
    def anime_id(self):
        return self.anime.id

    anime = factory.SubFactory(OrmAnimeFactory)
    week = 0
    watching = factory.Faker("pyint")
    completed = factory.Faker("pyint")
    dropped = factory.Faker("pyint")
    score = factory.Faker(
        "pyfloat"
    )  # min_value/max_value in Faker currently seem broken
    favorites = factory.Faker("pyint")
    total_forum_posts = factory.Faker("pyint")
    total_points = 0

    class Params:
        points_calculated = factory.Trait(total_points=factory.Faker("pyint"))
