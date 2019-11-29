import random

import factory

from .session import session_factory
from fal.orm import Season, Team


class OrmTeamFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Team
        sqlalchemy_session = session_factory

    id = factory.Sequence(lambda x: x)
    season_id = 0
    name = factory.Faker("user_name")
    mal_join_date = factory.Faker("date_time_this_decade", after_now=False)

    @factory.lazy_attribute_sequence
    def season(self, n):
        session = session_factory()
        _season = (
            session.query(Season).filter(Season.id == self.season_id).one_or_none()
        )

        if not _season:
            _season = Season(
                id=self.season_id,
                season_of_year=random.choice(["spring", "fall"]),
                year=2018 + n,
            )
            session.add(_season)
        return _season

    # fill these out later
    wildcards = []
    team_weekly_anime = []
