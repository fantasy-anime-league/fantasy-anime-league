import factory

from fal.controllers.anime_stats import AnimeStats


class AnimeStatsFactory(factory.Factory):
    class Meta:
        model = AnimeStats

    jikan_request_interval = 0
    current_week = 1

    simulcasts_filepath = ""
    licenses_filepath = ""
