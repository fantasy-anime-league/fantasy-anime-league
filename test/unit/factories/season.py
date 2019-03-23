import factory

from .session import session_factory
import fal.models


class SeasonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = fal.models.Season
        sqlalchemy_session = session_factory

    id = factory.Sequence(lambda x: x)
    season_of_year = factory.Faker('word', ext_word_list=['spring', 'fall'])
    year = factory.Faker('year')

    @factory.post_generation
    def anime(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of anime were passed in, use them
            for _anime in extracted:
                self.anime.add(_anime)  # pylint: disable=no-member

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of teams were passed in, use them
            self.teams += extracted
