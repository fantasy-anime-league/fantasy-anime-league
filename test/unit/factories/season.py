import factory

from .orm import OrmSeasonFactory
from fal.models import Season, SeasonOfYear


class SeasonFactory(factory.Factory):
    class Meta:
        model = Season

    @factory.lazy_attribute
    def entity(self):
        return OrmSeasonFactory(
            season_of_year=self.season_of_year.value, year=self.year
        )

    session = None
    season_of_year = SeasonOfYear.SPRING
    year = 2006
    current_week = 0
    min_weeks_between_bench_swaps = 3
